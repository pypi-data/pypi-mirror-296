import matplotlib.pyplot as plt
import numpy as np

from classifier_toolkit.feature_selection.base import BaseFeatureSelector


def plot_feature_importances(selector: BaseFeatureSelector) -> None:
    importances = selector.get_feature_importances().sort_values(ascending=True)

    plt.figure(figsize=(10, max(8, len(importances) * 0.3)))
    y_pos = np.arange(len(importances))
    plt.barh(y_pos, np.array(importances.values))
    plt.yticks(y_pos, importances.index.astype(str).tolist())
    plt.xlabel("Importance")
    plt.title("Feature Importances")
    plt.tight_layout()
    plt.show()


def plot_rfecv_results(selector: BaseFeatureSelector) -> None:
    assert hasattr(
        selector, "rfecv"
    ), "This plot is only available for RFECV-based selectors."
    assert (
        selector.rfecv is not None
    ), "RFECV results are not available. Make sure to fit the selector first."
    assert hasattr(
        selector.rfecv, "cv_results_"
    ), "The selector's RFECV doesn't have cv_results_. Make sure to fit the selector first."

    n_features_total = len(selector.get_feature_importances())

    grid_scores = selector.rfecv.cv_results_["mean_test_score"]
    std_errors = selector.rfecv.cv_results_["std_test_score"]

    n_features = np.arange(1, n_features_total + 1)

    plt.figure(figsize=(12, 6))
    plt.title("Feature Selection using RFECV")
    plt.xlabel("Number of features selected")
    plt.ylabel("Cross-validation score")
    plt.plot(n_features, grid_scores)
    plt.fill_between(
        n_features, grid_scores - std_errors, grid_scores + std_errors, alpha=0.2
    )
    plt.axvline(
        selector.rfecv.n_features_,
        color="red",
        linestyle="--",
        label=f"Optimal number of features ({selector.rfecv.n_features_})",
    )
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Plot feature importances
    importances = selector.get_feature_importances().sort_values(ascending=False)
    plt.figure(figsize=(12, 8))
    plt.title("Feature Importances")
    importances.plot(kind="bar")
    plt.xlabel("Features")
    plt.ylabel("Importance")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
