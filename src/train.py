"""
src/train.py
============
Module 5 – Model Training

Trains a Multinomial Naive Bayes classifier using a sklearn Pipeline
(TF-IDF → MultinomialNB) with stratified train/test split.

Mathematical Foundation – Bayes' Theorem:
  P(sentiment | text) ∝ P(sentiment) × ∏ P(word | sentiment)

  Naïve assumption: each word is conditionally independent given the class.
  Multinomial NB: counts word frequencies per class; uses Laplace smoothing.

Probability, Bayes' Theorem, Conditional Probability
Hyperparameter tuning (alpha = Laplace smoothing coefficient)
"""

import json
import os
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from src.config import (
    LABEL_COLUMN, METADATA_PATH, MODEL_PATH, NB_ALPHA,
    RANDOM_STATE, SENTIMENT_CLASSES, TEST_SIZE,
    TFIDF_MAX_DF, TFIDF_MAX_FEAT, TFIDF_MIN_DF, TFIDF_NGRAM,
)
from src.feature_extraction import build_tfidf_vectorizer


# ── Build sklearn Pipelines ───────────────────────────────────────────────────

def build_nb_pipeline(alpha: float = NB_ALPHA) -> Pipeline:
    """
    Build a TF-IDF + Multinomial Naive Bayes Pipeline.

    Using a Pipeline prevents data leakage:
      - TF-IDF is fit ONLY on training data.
      - Test data is transformed using the training vocabulary.

    No data leakage → Data Integrity.

    Args:
        alpha: Laplace smoothing parameter (Probability).
               alpha=1 → standard Laplace smoothing.
               alpha→0 → no smoothing (can cause zero probabilities).

    Returns:
        sklearn Pipeline (unfitted).
    """
    tfidf = build_tfidf_vectorizer()
    nb    = MultinomialNB(alpha=alpha)
    return Pipeline([("tfidf", tfidf), ("classifier", nb)])


def build_lr_pipeline() -> Pipeline:
    """
    Build a TF-IDF + Logistic Regression Pipeline.
    Used as an optional comparison model.

    Logistic Regression uses gradient descent (L-BFGS) to
    minimize cross-entropy loss — demonstrating optimization concepts.
    Naive Bayes uses direct probability estimation, NOT gradient descent.

    Returns:
        sklearn Pipeline (unfitted).
    """
    tfidf = build_tfidf_vectorizer()
    lr    = LogisticRegression(
        max_iter=1000,
        random_state=RANDOM_STATE,
        solver="lbfgs",
        C=1.0,
    )
    return Pipeline([("tfidf", tfidf), ("classifier", lr)])


# ── Train / Evaluate ──────────────────────────────────────────────────────────

def split_data(df: pd.DataFrame, text_col: str = "clean_text"):
    """
    Stratified train/test split.

    Stratification ensures class proportions are maintained in both splits.
    Sampling strategy, class imbalance.

    Args:
        df:       DataFrame with 'clean_text' and 'sentiment' columns.
        text_col: Column name for preprocessed text.

    Returns:
        X_train, X_test, y_train, y_test
    """
    X = df[text_col]
    y = df[LABEL_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size    = TEST_SIZE,
        random_state = RANDOM_STATE,
        stratify     = y,      # maintain class ratio in splits
    )
    print(f"[Train] Training samples : {len(X_train):,}")
    print(f"[Train] Testing  samples : {len(X_test):,}")
    return X_train, X_test, y_train, y_test


def train_model(
    X_train,
    y_train,
    pipeline: Pipeline = None,
    model_type: str = "naive_bayes",
) -> Pipeline:
    """
    Fit a pipeline on training data.

    Args:
        X_train:    Training texts (pd.Series).
        y_train:    Training labels (pd.Series).
        pipeline:   Pre-built pipeline; builds default NB if None.
        model_type: "naive_bayes" or "logistic_regression".

    Returns:
        Fitted Pipeline.
    """
    if pipeline is None:
        if model_type == "logistic_regression":
            pipeline = build_lr_pipeline()
        else:
            pipeline = build_nb_pipeline()

    print(f"[Train] Fitting {model_type} pipeline...")
    pipeline.fit(X_train, y_train)
    print("[Train] Training complete.")
    return pipeline


def cross_validate_model(pipeline: Pipeline, X, y, cv: int = 5) -> dict:
    """
    Perform k-fold cross-validation.

    Statistical reliability of model estimates.
    Cross-validation gives a more robust accuracy estimate than a single split.

    Args:
        pipeline: Unfitted (or freshly constructed) pipeline.
        X:        All text data.
        y:        All labels.
        cv:       Number of folds (default 5).

    Returns:
        dict with mean, std, and individual fold scores.
    """
    scores = cross_val_score(pipeline, X, y, cv=cv, scoring="accuracy", n_jobs=-1)
    return {
        "cv_folds":  cv,
        "scores":    scores.tolist(),
        "mean":      round(float(scores.mean()), 4),
        "std":       round(float(scores.std()),  4),
        "ci_lower":  round(float(scores.mean() - 2 * scores.std()), 4),
        "ci_upper":  round(float(scores.mean() + 2 * scores.std()), 4),
    }


# ── Save / Load ───────────────────────────────────────────────────────────────

def save_model(pipeline: Pipeline, metadata: dict,
               model_path: str = MODEL_PATH,
               meta_path: str  = METADATA_PATH):
    """
    Persist the fitted pipeline and metadata to disk.

    Model deployment using joblib serialisation.

    Args:
        pipeline:   Fitted sklearn Pipeline.
        metadata:   Dictionary of training metadata to save as JSON.
        model_path: Output path for the .pkl file.
        meta_path:  Output path for the metadata JSON.
    """
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(pipeline, model_path)
    print(f"[Train] Model saved   -> {model_path}")

    metadata["saved_at"] = datetime.now().isoformat()
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"[Train] Metadata saved -> {meta_path}")


def load_model(model_path: str = MODEL_PATH) -> Pipeline:
    """
    Load a previously saved pipeline from disk.

    Returns:
        Fitted sklearn Pipeline.

    Raises:
        FileNotFoundError if model file does not exist.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model file not found at: {model_path}\n"
            "Please train the model first via the training script."
        )
    pipeline = joblib.load(model_path)
    print(f"[Train] Model loaded <- {model_path}")
    return pipeline


def load_metadata(meta_path: str = METADATA_PATH) -> dict:
    """Load model training metadata from JSON."""
    if not os.path.exists(meta_path):
        return {}
    with open(meta_path) as f:
        return json.load(f)


def naive_bayes_explanation() -> str:
    """
    Return a formatted explanation of Multinomial Naive Bayes.
    Used in the About and Model Evaluation pages.
    """
    return """
### Multinomial Naive Bayes — Mathematical Explanation

**Bayes' Theorem**

$$P(C_k \\mid \\mathbf{x}) = \\frac{P(C_k) \\cdot P(\\mathbf{x} \\mid C_k)}{P(\\mathbf{x})}$$

Where:
- $C_k$ = sentiment class (Positive, Negative, Neutral)
- $\\mathbf{x}$ = feature vector of the input text
- $P(C_k)$ = prior probability of class $k$
- $P(\\mathbf{x} \\mid C_k)$ = likelihood of observing text given class

**Naïve Independence Assumption**

$$P(\\mathbf{x} \\mid C_k) = \\prod_{i=1}^{n} P(x_i \\mid C_k)$$

Each word is assumed to be independent given the class. While unrealistic,
this simplification makes computation tractable and works very well in practice.

**Multinomial Likelihood (with Laplace Smoothing)**

$$P(w \\mid C_k) = \\frac{\\text{count}(w, C_k) + \\alpha}{\\sum_w \\text{count}(w, C_k) + \\alpha \\cdot |V|}$$

Where:
- $\\alpha = 1$ → Laplace (add-one) smoothing prevents zero probabilities
- $|V|$ = vocabulary size

**Prediction**

$$\\hat{y} = \\arg\\max_{k} \\left[ \\log P(C_k) + \\sum_{i} \\log P(x_i \\mid C_k) \\right]$$

Log-space computation prevents numerical underflow when multiplying many small probabilities.

**Why Naive Bayes for Sentiment?**
- Fast training: O(n × |V|) — no gradient descent needed
- Works well on high-dimensional sparse TF-IDF features
- Interpretable: we can inspect P(word | class) directly
- Handles short texts robustly
"""

