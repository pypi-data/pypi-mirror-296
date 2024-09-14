from typing import List, Literal, Optional, Union

import pandas as pd
from tqdm import tqdm

from classifier_toolkit.feature_selection.base import (
    BaseFeatureSelector,
    FeatureSelectionError,
)
from classifier_toolkit.feature_selection.wrapper_methods.rfe import (
    EnsembleFeatureSelector,
)
from classifier_toolkit.feature_selection.wrapper_methods.sequential_selection import (
    SequentialSelector,
)


class MetaSelector(BaseFeatureSelector):
    """
    A meta-selector that combines multiple feature selection methods.

    This class allows for the combination of multiple feature selection methods
    using different voting strategies.

    Parameters
    ----------
    methods : Optional[List[BaseFeatureSelector]], optional
        List of feature selection methods to be combined, by default None.
    voting : str, optional
        The voting strategy to use for combining methods, by default "majority".
        Options are "majority", "union", or "intersection".
    n_features_to_select : Optional[int], optional
        The number of features to select, by default None.
    scoring : str, optional
        The scoring metric to use, by default "accuracy".
    cv : int, optional
        The number of cross-validation folds, by default 5.
    verbose : int, optional
        Verbosity level, by default 0.

    Attributes
    ----------
    methods : List[BaseFeatureSelector]
        The list of feature selection methods.
    voting : str
        The voting strategy used.
    feature_importances_ : pd.Series
        The combined feature importances.
    selected_features_ : List[str]
        The list of selected features.

    Raises
    ------
    ValueError
        If any of the provided methods is not an instance of BaseFeatureSelector.
    """

    def __init__(
        self,
        methods: Optional[List[BaseFeatureSelector]] = None,
        voting: Literal["majority", "union", "intersection"] = "majority",
        n_features_to_select: int = 1,
        scoring: Literal[
            "accuracy", "f1", "precision", "recall", "roc_auc"
        ] = "accuracy",
        cv: int = 5,
        verbose: int = 0,
    ):
        super().__init__(
            estimator=None,  # MetaSelector doesn't need its own estimator
            n_features_to_select=n_features_to_select,
            scoring=scoring,
            cv=cv,
            verbose=verbose,
        )
        self.methods = methods or [
            EnsembleFeatureSelector(
                estimator="random_forest",
                n_features_to_select=self.n_features_to_select,
            ),
            SequentialSelector(
                method="forward",
                estimator_name="lightgbm",
                estimator_params={"n_estimators": 100},
                n_features_to_select=self.n_features_to_select,
            ),
        ]
        if not all(isinstance(method, BaseFeatureSelector) for method in self.methods):
            raise ValueError("All methods must be instances of BaseFeatureSelector")
        self.voting = voting

    def fit(self, X: pd.DataFrame, y: pd.Series) -> "MetaSelector":
        """
        Fit the MetaSelector to the data.

        This method fits all the individual feature selection methods and then
        combines their results based on the specified voting strategy.

        Parameters
        ----------
        X : pd.DataFrame
            The input features.
        y : pd.Series
            The target variable.

        Returns
        -------
        MetaSelector
            The fitted MetaSelector instance.

        Raises
        ------
        ValueError
            If an invalid voting strategy is specified.
        """
        # Create a progress bar
        pbar = tqdm(total=len(self.methods), desc="Fitting methods")

        for i, method in enumerate(self.methods):
            print(
                f"\nFitting method {i+1}/{len(self.methods)}: {type(method).__name__}"
            )
            method.fit(X, y)
            # Update the progress bar
            pbar.update(1)
            pbar.set_description(f"Fitted {type(method).__name__}")

        # Close the progress bar
        pbar.close()

        self._combine_feature_importances()

        if self.voting == "majority":
            self._majority_voting()
        elif self.voting == "union":
            self._union_voting()
        elif self.voting == "intersection":
            self._intersection_voting()
        else:
            raise ValueError("Voting must be 'majority', 'union', or 'intersection'")

        return self

    def _combine_feature_importances(self):
        all_importances = [method.get_feature_importances() for method in self.methods]
        combined_importances = pd.concat(all_importances, axis=1)

        if self.voting == "majority":
            self.feature_importances_ = combined_importances.mean(axis=1)
        elif self.voting == "union" or self.voting == "intersection":
            self.feature_importances_ = combined_importances.max(axis=1)

        self.feature_importances_ = self.feature_importances_.sort_values(
            ascending=False
        )

    def print_feature_importances(self):
        if self.feature_importances_ is None:
            raise FeatureSelectionError(
                "Feature importances are not available. Call 'fit' first."
            )

        print("Combined Feature Importances (in descending order):")
        for feature, importance in self.feature_importances_.items():
            print(f"('{feature}', {importance:.6f})")

    def get_feature_importances(self) -> pd.Series:
        """
        Get the combined feature importances.

        Returns
        -------
        pd.Series
            The combined feature importances.

        Raises
        ------
        FeatureSelectionError
            If the selector has not been fitted yet.
        """
        if self.feature_importances_ is None:
            raise FeatureSelectionError(
                "Selector has not been fitted yet. Call 'fit' first."
            )
        return self.feature_importances_

    def _majority_voting(self):
        all_importances = [method.get_feature_importances() for method in self.methods]
        combined_importances = pd.concat(all_importances, axis=1)
        threshold = len(self.methods) / 2
        feature_counts = (combined_importances > 0).sum(axis=1)
        self.selected_features_ = list(feature_counts[feature_counts > threshold].index)
        self.feature_importances_ = combined_importances.loc[
            self.selected_features_
        ].mean(axis=1)

    def _union_voting(self):
        all_selected = [set(method.selected_features_) for method in self.methods]
        union_features = set.union(*all_selected)
        self.selected_features_ = list(union_features)
        all_importances = [method.get_feature_importances() for method in self.methods]
        combined_importances = pd.concat(all_importances, axis=1)
        self.feature_importances_ = combined_importances.loc[
            self.selected_features_
        ].mean(axis=1)

    def _intersection_voting(self):
        all_selected = [set(method.selected_features_) for method in self.methods]
        intersection_features = set.intersection(*all_selected)
        self.selected_features_ = list(intersection_features)
        all_importances = [method.get_feature_importances() for method in self.methods]
        combined_importances = pd.concat(all_importances, axis=1)
        self.feature_importances_ = combined_importances.loc[
            self.selected_features_
        ].mean(axis=1)

    def print_results(self):
        """
        Print the results of the feature selection process.

        This method prints the results of individual methods, the combined results
        based on voting, and the final feature importances.
        """
        print("Individual method results:")
        for method in self.methods:
            print(f"{type(method).__name__}: {method.selected_features_}")

        print("\nCombined results based on voting:")
        print(f"Voting method: {self.voting}")
        print(f"Selected features: {self.selected_features_}")

        print("\nFinal feature importances:")
        for feature, importance in self.feature_importances_.sort_values(
            ascending=False
        ).items():
            print(f"('{feature}', {importance:.6f})")

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transform the input data by selecting the chosen features.

        Parameters
        ----------
        X : pd.DataFrame
            The input features.

        Returns
        -------
        pd.DataFrame
            The transformed data containing only the selected features.

        Raises
        ------
        FeatureSelectionError
            If the selector has not been fitted yet.
        """
        if self.selected_features_ is None:
            raise FeatureSelectionError(
                "Selector has not been fitted yet. Call 'fit' first."
            )
        return X[self.selected_features_]

    def fit_transform(self, X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
        """
        Fit the MetaSelector to the data and then transform it.

        Parameters
        ----------
        X : pd.DataFrame
            The input features.
        y : pd.Series
            The target variable.

        Returns
        -------
        pd.DataFrame
            The transformed data containing only the selected features.
        """
        return self.fit(X, y).transform(X)

    def get_support(self, indices: bool = False) -> Union[List[bool], List[int]]:
        """
        Get a boolean mask or integer index array indicating the selected features.

        Parameters
        ----------
        indices : bool, optional
            If True, returns an integer index array, otherwise returns a boolean mask.

        Returns
        -------
        Union[List[bool], List[int]]
            Boolean mask or integer index array indicating the selected features.

        Raises
        ------
        FeatureSelectionError
            If the selector has not been fitted yet.
        """
        if self.selected_features_ is None:
            raise FeatureSelectionError(
                "Selector has not been fitted yet. Call 'fit' first."
            )
        assert self.feature_importances_ is not None, ValueError(
            'Feature importances are not available. Call "fit" first.'
        )
        mask = [
            feature in self.selected_features_
            for feature in self.feature_importances_.index
        ]
        if indices:
            return [i for i, m in enumerate(mask) if m]
        return mask

    def get_individual_results(self):
        """
        Get the results of individual feature selection methods.

        Returns
        -------
        dict
            A dictionary containing the selected features for each method.
        """
        return {
            type(method).__name__: method.selected_features_ for method in self.methods
        }

    def _get_score(self, X: pd.DataFrame, y: pd.Series, features: List[int]) -> float:
        raise NotImplementedError
