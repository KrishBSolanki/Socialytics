"""
src/prediction.py
=================
Module 7 – Real-Time and Batch Prediction

Provides:
  • Single text prediction with probabilities
  • Batch prediction for DataFrames (bulk CSV analysis)
  • Prediction caching for performance
  • Input validation and sanitisation

Data Science Life Cycle — Deployment & Prediction stage
"""

import os
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from src.config import SENTIMENT_CLASSES, TEXT_COLUMN
from src.preprocessing import clean_text
from src.train import load_model


# ── Module-level model cache ──────────────────────────────────────────────────
_cached_pipeline: Optional[Pipeline] = None


def get_pipeline(model_path: str = None) -> Pipeline:
    """
    Return the loaded pipeline, loading from disk only once per session.

    Load model once; do not retrain on each page refresh.
    """
    global _cached_pipeline
    if _cached_pipeline is None:
        if model_path:
            _cached_pipeline = load_model(model_path)
        else:
            _cached_pipeline = load_model()
    return _cached_pipeline


def predict_single(text: str, pipeline: Pipeline = None) -> Dict:
    """
    Predict sentiment for a single text input.

    Args:
        text:     Raw input text (user-entered review/comment).
        pipeline: Optional pre-loaded pipeline.

    Returns:
        dict with keys:
          - raw_text:        original input
          - clean_text:      preprocessed text
          - sentiment:       predicted class label
          - probabilities:   dict {class: probability}
          - confidence:      max probability (not a guaranteed certainty)
          - warning:         any validation warnings

    Raises:
        ValueError: if text is empty after cleaning.
    """
    if pipeline is None:
        pipeline = get_pipeline()

    warnings = []

    # ── Input Validation ──────────────────────────────────────────────────
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    text = text.strip()

    if len(text) == 0:
        raise ValueError("Input text is empty. Please enter a review or comment.")

    if len(text) < 3:
        raise ValueError("Input text is too short. Please enter at least 3 characters.")

    if len(text) > 5000:
        text = text[:5000]
        warnings.append("Input was truncated to 5000 characters.")

    # ── Preprocessing ─────────────────────────────────────────────────────
    cleaned = clean_text(text)

    if len(cleaned.strip()) == 0:
        warnings.append("Text contained only special characters after cleaning. "
                        "Prediction may be unreliable.")
        cleaned = text.lower()   # fallback: use lowercased original

    # ── Prediction ────────────────────────────────────────────────────────
    classes = pipeline.classes_
    proba   = pipeline.predict_proba([cleaned])[0]
    pred    = pipeline.predict([cleaned])[0]

    prob_dict = {cls: round(float(p), 4) for cls, p in zip(classes, proba)}
    confidence = round(float(max(proba)), 4)

    if confidence < 0.50:
        warnings.append(
            f"Model confidence is low ({confidence:.0%}). "
            "This prediction may be less reliable."
        )

    return {
        "raw_text":     text,
        "clean_text":   cleaned,
        "sentiment":    pred,
        "probabilities":prob_dict,
        "confidence":   confidence,
        "warning":      "; ".join(warnings) if warnings else None,
    }


def predict_batch(
    df: pd.DataFrame,
    text_col: str = TEXT_COLUMN,
    pipeline: Pipeline = None,
) -> pd.DataFrame:
    """
    Predict sentiment for every row in a DataFrame.

    Used by Module 8 (Bulk CSV Analysis).

    Args:
        df:       DataFrame containing text data.
        text_col: Column with text to analyse.
        pipeline: Optional pre-loaded pipeline.

    Returns:
        DataFrame with added columns:
          clean_text, predicted_sentiment, prob_Positive, prob_Negative, prob_Neutral, confidence
    """
    if pipeline is None:
        pipeline = get_pipeline()

    result_df = df.copy()

    # Validate column
    if text_col not in result_df.columns:
        raise ValueError(f"Column '{text_col}' not found in uploaded file.")

    # Preprocess
    result_df["clean_text"] = result_df[text_col].fillna("").apply(clean_text)

    # Handle empty cleaned texts
    empty_mask = result_df["clean_text"].str.strip().str.len() == 0
    result_df.loc[empty_mask, "clean_text"] = (
        result_df.loc[empty_mask, text_col].fillna("").str.lower()
    )

    # Predict
    texts   = result_df["clean_text"].tolist()
    probas  = pipeline.predict_proba(texts)
    preds   = pipeline.predict(texts)
    classes = pipeline.classes_

    result_df["predicted_sentiment"] = preds

    for i, cls in enumerate(classes):
        result_df[f"prob_{cls}"] = probas[:, i].round(4)

    result_df["confidence"] = probas.max(axis=1).round(4)

    return result_df

