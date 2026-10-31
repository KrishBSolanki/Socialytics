"""
src/evaluation.py
=================
Module 6 – Model Evaluation

Computes:
  • Accuracy, Precision, Recall, F1-score (macro & weighted)
  • Confusion Matrix
  • Classification Report
  • Cross-validation statistics
  • Optional: Comparison between NB and Logistic Regression

Statistics, hypothesis testing, confidence intervals
Model evaluation as part of capstone project
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from src.config import SENTIMENT_CLASSES


def compute_metrics(y_true, y_pred, labels=None) -> dict:
    """
    Compute comprehensive classification metrics.

    Metrics Explained:
      Accuracy  = (TP + TN) / total
      Precision = TP / (TP + FP)  — of those predicted positive, how many are?
      Recall    = TP / (TP + FN)  — of all actual positives, how many did we catch?
      F1-score  = 2 × (P × R) / (P + R)  — harmonic mean of Precision and Recall

    Args:
        y_true:  Ground-truth labels.
        y_pred:  Model predictions.
        labels:  Class ordering for the report.

    Returns:
        dict with scalar metrics and per-class breakdown.
    """
    if labels is None:
        labels = sorted(set(y_true) | set(y_pred))

    acc      = accuracy_score(y_true, y_pred)
    prec_mac = precision_score(y_true, y_pred, average="macro",    zero_division=0, labels=labels)
    rec_mac  = recall_score(y_true, y_pred,    average="macro",    zero_division=0, labels=labels)
    f1_mac   = f1_score(y_true, y_pred,        average="macro",    zero_division=0, labels=labels)
    prec_wtd = precision_score(y_true, y_pred, average="weighted", zero_division=0, labels=labels)
    rec_wtd  = recall_score(y_true, y_pred,    average="weighted", zero_division=0, labels=labels)
    f1_wtd   = f1_score(y_true, y_pred,        average="weighted", zero_division=0, labels=labels)

    cm       = confusion_matrix(y_true, y_pred, labels=labels)
    report   = classification_report(y_true, y_pred, labels=labels,
                                     output_dict=True, zero_division=0)

    return {
        "accuracy":          round(acc, 4),
        "precision_macro":   round(prec_mac, 4),
        "recall_macro":      round(rec_mac, 4),
        "f1_macro":          round(f1_mac, 4),
        "precision_weighted":round(prec_wtd, 4),
        "recall_weighted":   round(rec_wtd, 4),
        "f1_weighted":       round(f1_wtd, 4),
        "confusion_matrix":  cm.tolist(),
        "labels":            labels,
        "classification_report": report,
    }


def confusion_matrix_df(metrics: dict) -> pd.DataFrame:
    """Convert confusion matrix list to a labelled DataFrame."""
    cm     = np.array(metrics["confusion_matrix"])
    labels = metrics["labels"]
    return pd.DataFrame(cm, index=labels, columns=labels)


def metrics_explanation() -> str:
    """Return a simple language explanation of evaluation metrics."""
    return """
### Understanding Evaluation Metrics

| Metric | Formula | What it measures |
|--------|---------|-----------------|
| **Accuracy** | (TP + TN) / Total | Overall correctness |
| **Precision** | TP / (TP + FP) | When we predict a class, how often are we right? |
| **Recall** | TP / (TP + FN) | Of all real instances of a class, how many did we find? |
| **F1-Score** | 2PR / (P + R) | Harmonic mean — balances Precision and Recall |

**Why not rely on Accuracy alone?**
With imbalanced classes (e.g. 70% Positive), a model predicting "Positive"
for everything achieves 70% accuracy but is useless.
F1-score penalises such behaviour.

**Macro vs Weighted F1:**
- **Macro**: average F1 across classes, treating each class equally.
- **Weighted**: average F1 weighted by class support (number of samples).
  Better when class sizes differ significantly.

**Confusion Matrix:** Rows = Actual class, Columns = Predicted class.
Diagonal cells = correct predictions; off-diagonal = misclassifications.
"""

