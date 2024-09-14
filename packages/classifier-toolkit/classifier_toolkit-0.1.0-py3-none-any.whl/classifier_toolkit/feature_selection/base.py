from abc import ABC, abstractmethod
from typing import List, Literal, Optional, Union

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_selection import RFECV
from sklearn.model_selection import BaseCrossValidator, cross_val_score
from sklearn.utils import check_X_y


class BaseFeatureSelector(BaseEstimator, TransformerMixin, ABC):
    @abstractmethod
    def __init__(
        self,
        estimator: Optional[BaseEstimator],
        n_features_to_select: int = 1,
        scoring: Literal[
            "accuracy", "f1", "precision", "recall", "roc_auc"
        ] = "accuracy",
        cv: Union[int, BaseCrossValidator] = 5,
        verbose: int = 0,
    ) -> None:
        self.estimator: Optional[BaseEstimator] = estimator
        self.n_features_to_select = n_features_to_select
        self.scoring = scoring
        from .utils.scoring import get_scorer

        self.scorer = get_scorer(scoring)
        self.cv = cv
        self.verbose = verbose
        self.selected_features_: Optional[List[str]] = None
        self.feature_importances_: Optional[pd.Series] = None
        self.rfecv: Optional[RFECV] = None
        self.rfecv_step: int = 1

    @abstractmethod
    def fit(self, X: pd.DataFrame, y: pd.Series) -> "BaseFeatureSelector":
        """
        Fit the feature selector to the data.
        """

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transform the data to include only selected features.
        """
        if self.selected_features_ is None:
            raise FeatureSelectionError(
                "Selector has not been fitted yet. Call 'fit' first."
            )
        if isinstance(self.selected_features_[0], str):
            return X[self.selected_features_]
        else:
            return X.loc[:, self.selected_features_]

    def fit_transform(self, X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
        """
        Fit the selector and transform the data.
        """
        return self.fit(X, y).transform(X)

    @abstractmethod
    def _get_score(self, X: pd.DataFrame, y: pd.Series, features: List[int]) -> float:
        """
        Evaluate the score for a subset of features.

        Args:
            X (pd.DataFrame): The input features.
            y (pd.Series): The target variable.
            features (List[int]): The indices of features to evaluate.

        Returns:
            float: The score for the given features.
        """

    @abstractmethod
    def get_feature_importances(self) -> pd.Series:
        """
        Get the importance scores for each feature.
        """

    def get_support(self, indices: bool = False) -> Union[List[bool], List[int]]:
        """
        Get a mask, or integer index, of the features selected.
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

    def _evaluate_features(
        self, X: Union[pd.DataFrame, np.ndarray], y: pd.Series
    ) -> pd.Series:
        """
        Evaluate the features using cross-validation.

        Args:
            X (Union[pd.DataFrame, np.ndarray]): The input features.
            y (pd.Series): The target variable.

        Returns:
            pd.Series: A series containing the mean cross-validation score for each feature.
        """
        if self.estimator is None:
            raise ValueError("Estimator is not set. Please provide an estimator.")

        X, y = check_X_y(X, y, ensure_min_features=0, force_all_finite=False)

        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])

        scores = []
        feature_names = X.columns

        for feature in feature_names:
            X_feature = X[[feature]]
            try:
                feature_scores = cross_val_score(
                    self.estimator,
                    X_feature,
                    y,
                    scoring=self.scorer,
                    cv=self.cv,
                    n_jobs=-1,
                    error_score="raise",
                )
                mean_score = np.mean(feature_scores)
            except Exception as e:
                if self.verbose > 0:
                    print(f"Error evaluating feature {feature}: {e!s}")
                mean_score = np.nan

            scores.append(mean_score)

        return pd.Series(scores, index=feature_names, name="Feature Scores")

    def fit_rfecv(
        self, X: pd.DataFrame, y: pd.Series, **rfecv_params
    ) -> "BaseFeatureSelector":
        """
        Fit the selector using RFECV.

        Args:
            X (pd.DataFrame): The input features.
            y (pd.Series): The target variable.
            **rfecv_params: Additional parameters to  to RFECV.

        Returns:
            self: The fitted selector.
        """
        if self.estimator is None:
            raise ValueError("Estimator is not set. Please provide an estimator.")

        self.rfecv = RFECV(
            estimator=self.estimator,
            step=self.rfecv_step,
            cv=self.cv,
            scoring=self.scoring,
            n_jobs=-1,
            verbose=self.verbose,
            **rfecv_params,
        )

        self.rfecv.fit(X, y)
        self.selected_features_ = X.columns[self.rfecv.support_].tolist()
        self.feature_importances_ = pd.Series(self.rfecv.ranking_, index=X.columns)

        return self


class FeatureSelectionError(Exception):
    """Base exception for feature selection errors."""
