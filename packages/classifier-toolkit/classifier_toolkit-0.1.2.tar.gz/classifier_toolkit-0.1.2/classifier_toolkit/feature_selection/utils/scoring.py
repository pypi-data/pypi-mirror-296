from typing import Callable, Dict, Union

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    make_scorer,
    precision_score,
    recall_score,
    roc_auc_score,
)

# Define a dictionary of scoring functions
SCORING_FUNCTIONS: Dict[str, Callable] = {
    "accuracy": accuracy_score,
    "f1": f1_score,
    "precision": precision_score,
    "recall": recall_score,
    "roc_auc": roc_auc_score,
    # add prauc to the scoring functions, and make it default in the Literal call
}


def get_scorer(metric: Union[str, Callable]) -> Callable:
    """
    Get a scorer function for the given metric.

    Args:
        metric (str or callable): The metric to use for scoring.
                                  If string, must be one of the keys in SCORING_FUNCTIONS.
                                  If callable, should be a custom scoring function.

    Returns:
        A scorer function that can be used with scikit-learn's cross-validation and model selection tools.

    Raises:
        ValueError: If the metric is not recognized.
    """
    if isinstance(metric, str):
        if metric not in SCORING_FUNCTIONS:
            raise ValueError(
                f"Unrecognized metric: {metric}. Available metrics are: {', '.join(SCORING_FUNCTIONS.keys())}"
            )
        return make_scorer(SCORING_FUNCTIONS[metric])
    elif callable(metric):
        return make_scorer(metric)
    else:
        raise ValueError("metric must be either a string or a callable")


def false_positive_rate(y_true: int, y_pred: int) -> float:
    """
    Calculate the false positive rate.

    Args:
        y_true: True labels
        y_pred: Predicted labels

    Returns:
        False positive rate
    """
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return fp / (fp + tn)


def true_positive_rate(y_true: int, y_pred: int):
    """
    Calculate the true positive rate (also known as recall or sensitivity).

    Args:
        y_true: True labels
        y_pred: Predicted labels

    Returns:
        True positive rate
    """
    return recall_score(y_true, y_pred)


# Add FPR and TPR to the scoring functions
SCORING_FUNCTIONS["fpr"] = false_positive_rate
SCORING_FUNCTIONS["tpr"] = true_positive_rate

# Create scorers for FPR and TPR
fpr_scorer = make_scorer(false_positive_rate, greater_is_better=False)
tpr_scorer = make_scorer(true_positive_rate, greater_is_better=True)
