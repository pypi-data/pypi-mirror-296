from typing import List, Optional

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.linear_model import ElasticNetCV, LogisticRegression
from sklearn.model_selection import cross_val_score

from classifier_toolkit.feature_selection.base import (
    BaseFeatureSelector,
    FeatureSelectionError,
)


class ElasticNetSelector(BaseFeatureSelector):
    """
    Feature selector based on Elastic Net regularization.

    This class implements feature selection using Elastic Net, which combines
    L1 and L2 regularization.

    Parameters
    ----------
    estimator : Optional[BaseEstimator], optional
        The estimator to use, by default None.
    l1_ratio : float, optional
        The ElasticNet mixing parameter, by default 0.5.
    max_iter : int, optional
        Maximum number of iterations, by default 10000.
    **kwargs
        Additional keyword arguments to be passed to the BaseFeatureSelector.

    Attributes
    ----------
    l1_ratio : float
        The ElasticNet mixing parameter.
    max_iter : int
        Maximum number of iterations.
    model : Optional[ElasticNetCV]
        The fitted ElasticNetCV model.
    feature_importances_ : pd.Series
        The feature importances (coefficients) from the fitted model.
    selected_features_ : List[str]
        The list of selected features.
    """

    def __init__(
        self,
        estimator: Optional[BaseEstimator] = None,
        l1_ratio: float = 0.5,
        max_iter: int = 10000,
        **kwargs,
    ) -> None:
        # Use LogisticRegression as the default estimator if none is provided
        if estimator is None:
            estimator = LogisticRegression(random_state=42)
        super().__init__(estimator=estimator, **kwargs)
        self.l1_ratio = l1_ratio
        self.max_iter = max_iter
        self.model: Optional[ElasticNetCV] = None

    def fit(self, X: pd.DataFrame, y: pd.Series) -> "ElasticNetSelector":
        """
        Fit the ElasticNetSelector to the data.

        Parameters
        ----------
        X : pd.DataFrame
            The input features.
        y : pd.Series
            The target variable.

        Returns
        -------
        ElasticNetSelector
            The fitted ElasticNetSelector instance.

        Raises
        ------
        ValueError
            If model fitting fails or coefficients are not available.
        """
        self.model = ElasticNetCV(
            l1_ratio=self.l1_ratio, cv=self.cv, max_iter=self.max_iter
        ).fit(X, y)  # type: ignore
        if self.model is not None and hasattr(self.model, "coef_"):
            self.feature_importances_ = pd.Series(
                abs(self.model.coef_), index=X.columns
            )
            if self.feature_importances_ is not None:
                self.selected_features_ = self.feature_importances_[
                    self.feature_importances_ > 0
                ].index.tolist()
            else:
                raise ValueError("Feature importances are None after fitting.")
        else:
            raise ValueError("Model fitting failed or coefficients are not available.")
        return self

    def get_feature_importances(self) -> pd.Series:
        """
        Get the feature importances (coefficients) from the fitted model.

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

        Raises
        ------
        ValueError
            If the estimator is not set.
        """
        if self.estimator is None:
            raise ValueError("Estimator is not set. Please provide an estimator.")

        X_subset = X.iloc[:, features]
        scores = cross_val_score(
            self.estimator,
            X_subset,
            y,
            scoring=self.scorer,
            cv=self.cv,
            n_jobs=-1,
            error_score="raise",
        )
        return float(np.mean(scores))

    def return_feature_importances(self):
        """
        Print the feature importances (coefficients) in descending order of absolute value.

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
            key=lambda x: abs(x[1]),  # Sort by absolute value of coefficients
            reverse=True,
        )

        return sorted_importances
