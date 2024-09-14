from typing import List, Literal, Optional

import pandas as pd
from catboost import (
    CatBoostClassifier,
    EFeaturesSelectionAlgorithm,
    EShapCalcType,
    Pool,
)
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFECV
from xgboost import XGBClassifier

from classifier_toolkit.feature_selection.base import (
    BaseFeatureSelector,
    FeatureSelectionError,
)
from classifier_toolkit.feature_selection.utils.plottings import plot_rfecv_results


class EnsembleFeatureSelector(BaseFeatureSelector):
    """
    A feature selector that uses ensemble methods for feature selection.

    This class implements feature selection using various ensemble methods such as
    LightGBM, XGBoost, Random Forest, and CatBoost. It supports both Recursive Feature
    Elimination (RFE) and CatBoost's built-in feature selection.

    Parameters
    ----------
    estimator : {"xgboost", "random_forest", "lightgbm", "catboost"}, default="lightgbm"
        The estimator to use for feature selection.
    n_features_to_select : int, optional
        The number of features to select. If None, half of the features are selected.
    scoring : {"accuracy", "f1", "precision", "recall", "roc_auc"}, default="roc_auc"
        The scoring metric to use for feature selection.
    cv : int, default=5
        The number of cross-validation folds.
    verbose : int, default=0
        Controls the verbosity of the feature selection process.
    method : str, default="rfe"
        The feature selection method to use. Either "rfe" or "catboost".
    step : int, default=1
        The number of features to remove at each iteration for RFE.
    n_jobs : int, default=-1
        The number of jobs to run in parallel. -1 means using all processors.
    catboost_params : dict, optional
        Additional parameters for CatBoost.
    min_features_to_select : int, default=1
        The minimum number of features to select.

    Attributes
    ----------
    estimator_name : str
        The name of the estimator used.
    estimator : object
        The estimator object.
    selected_features_ : list
        The list of selected feature names after fitting.
    feature_importances_ : pd.Series
        The importance scores for each feature after fitting.
    rfecv : RFECV
        The RFECV object if RFE method is used.

    Methods
    -------
    fit(X, y)
        Fit the feature selector to the data.
    transform(X)
        Transform the data to include only selected features.
    get_feature_importances()
        Get the importance scores for each feature.
    print_feature_importances()
        Print the feature importances in descending order.
    """

    def __init__(
        self,
        estimator: Literal[
            "xgboost", "random_forest", "lightgbm", "catboost"
        ] = "lightgbm",
        n_features_to_select: int = 1,
        scoring: Literal[
            "accuracy", "f1", "precision", "recall", "roc_auc"
        ] = "roc_auc",
        cv: int = 5,
        verbose: int = 0,
        method: str = "rfe",
        step: int = 1,
        n_jobs: int = -1,
        catboost_params: Optional[dict] = None,
        min_features_to_select: int = 1,
        **kwargs,
    ) -> None:
        self.catboost_params = catboost_params or {}
        self.estimator_name = estimator
        self.estimator = self._get_estimator(estimator)  # type: ignore
        super().__init__(
            estimator=self.estimator,
            n_features_to_select=n_features_to_select,
            scoring=scoring,
            cv=cv,
            verbose=verbose,
            **kwargs,
        )
        self.method = method
        self.step = step
        self.n_jobs = n_jobs
        self.min_features_to_select = min_features_to_select

    def _get_estimator(self, estimator_name):
        """
        Get the estimator based on the provided name.

        Parameters
        ----------
        estimator_name : str
            The name of the estimator to use.

        Returns
        -------
        object
            The initialized estimator.

        Raises
        ------
        ValueError
            If the estimator name is not recognized.
        """
        if estimator_name == "lightgbm":
            return LGBMClassifier()
        elif estimator_name == "xgboost":
            return XGBClassifier()
        elif estimator_name == "random_forest":
            return RandomForestClassifier()
        elif estimator_name == "catboost":
            return CatBoostClassifier(**self.catboost_params)
        else:
            raise ValueError(f"Unknown estimator: {estimator_name}")

    def fit(self, X: pd.DataFrame, y: pd.Series) -> "EnsembleFeatureSelector":
        """
        Fit the feature selector to the data.

        Parameters
        ----------
        X : pd.DataFrame
            The input features.
        y : pd.Series
            The target variable.

        Returns
        -------
        EnsembleFeatureSelector
            The fitted feature selector.
        """
        if self.estimator_name == "catboost":
            self._fit_catboost(X, y)
        elif self.method == "rfe":
            self._fit_rfe(X, y)
        else:
            raise ValueError(
                "Invalid method. Choose 'rfe' or use 'catboost' estimator."
            )

        return self

    def _fit_rfe(self, X: pd.DataFrame, y: pd.Series) -> None:
        """
        Fit the RFE method to the data.

        Parameters
        ----------
        X : pd.DataFrame
            The input features.
        y : pd.Series
            The target variable.

        Raises
        ------
        ValueError
            If the estimator is not provided.
        """
        if self.estimator is None:
            raise ValueError("Estimator must be provided for RFE method")
        self.rfecv = RFECV(
            estimator=self.estimator,
            step=self.step,
            cv=self.cv,
            scoring=self.scoring,
            n_jobs=self.n_jobs,
            verbose=self.verbose,
            min_features_to_select=self.min_features_to_select,
        )
        self.rfecv.fit(X, y)
        self.selected_features_ = X.columns[self.rfecv.support_].tolist()
        self.feature_importances_ = pd.Series(self.rfecv.ranking_, index=X.columns)

    def _fit_catboost(self, X: pd.DataFrame, y: pd.Series) -> None:
        """
        Fit the CatBoost method to the data.

        Parameters
        ----------
        X : pd.DataFrame
            The input features.
        y : pd.Series
            The target variable.
        """
        model = CatBoostClassifier(**self.catboost_params)

        # Create CatBoost Pool objects
        train_pool = Pool(X, y)

        # Calculate the number of features to select
        nb_features = X.shape[1]
        features_select = (
            nb_features - 1
            if self.n_features_to_select is None
            else self.n_features_to_select
        )

        # Run feature selection
        summary = model.select_features(
            train_pool,
            eval_set=None,  # We're not using a separate evaluation set here
            features_for_select=f"0-{nb_features - 1}",
            num_features_to_select=features_select,
            algorithm=EFeaturesSelectionAlgorithm.RecursiveByShapValues,
            shap_calc_type=EShapCalcType.Regular,
            train_final_model=False,
            logging_level="Silent",
            plot=True,
        )

        # Extract selected features and their importances
        self.selected_features_ = [X.columns[i] for i in summary["selected_features"]]

        print(summary)

    def get_feature_importances(self) -> pd.Series:
        """
        Get the feature importances (scores) from the fitted model.

        Returns
        -------
        pd.Series
            The feature importances.

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

    def _get_score(self, X: pd.DataFrame, y: pd.Series, features: List[int]) -> float:
        """
        Calculate the cross-validation score for a subset of features.

        Parameters
        ----------
        X : pd.DataFrame
            The input features.
        y : pd.Series
            The target variable.
        features : List[int]
            The indices of features to use.

        Returns
        -------
        float
            The mean cross-validation score.
        """
        X_subset = X.iloc[:, features]
        self.estimator.fit(X_subset, y)  # type: ignore
        return self.scorer(self.estimator, X_subset, y)

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

    def plot_results(self) -> None:
        """
        Plot the results of the RFECV feature selection process.

        Raises
        ------
        ValueError
            If the RFECV results are not available.
        """
        try:
            plot_rfecv_results(self)
        except ValueError as e:
            print(f"Error plotting RFECV results: {e}")

    def print_feature_importances(self):
        """
        Print the feature importances (scores) in descending order.

        Raises
        ------
        FeatureSelectionError
            If feature importances are not available (i.e., fit hasn't been called).
        """
        if self.feature_importances_ is None:
            raise FeatureSelectionError(
                "Feature importances are not available. Call 'fit' first."
            )

        sorted_importances = sorted(
            zip(self.feature_importances_.index, self.feature_importances_),
            key=lambda x: x[1],
            reverse=True,
        )

        print("Feature importances (in descending order):")
        for feature, importance in sorted_importances:
            print(f"('{feature}', {importance:.6f})")
