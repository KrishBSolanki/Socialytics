"""
src/feature_extraction.py
=========================
Module 4 – TF-IDF Feature Extraction

Mathematical Foundation:
  TF(t, d)  = count(t in d) / total_terms(d)
  IDF(t)    = log( (1 + N) / (1 + df(t)) ) + 1   [sklearn smooth IDF]
  TF-IDF(t,d) = TF(t, d) × IDF(t)

Why TF-IDF?
  • Raw word counts favour longer documents.
  • TF-IDF down-weights common words (e.g. "the", "is") and
    up-weights rare but informative words.
  • Converts text → dense numerical feature vector for ML models.

Document-term matrix, feature vectors (Linear Algebra I)
Sparse matrix representation, optional TruncatedSVD
"""

import json
import os

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.decomposition import TruncatedSVD

from src.config import (
    TFIDF_MAX_FEAT, TFIDF_MIN_DF, TFIDF_MAX_DF, TFIDF_NGRAM,
    VECTORIZER_PATH, RANDOM_STATE
)


def build_tfidf_vectorizer(**kwargs) -> TfidfVectorizer:
    """
    Create a configured TfidfVectorizer instance.

    Key Parameters (explanation):
      max_features : vocabulary ceiling — keeps the top N features by TF-IDF score.
      min_df       : ignore terms appearing in fewer than min_df documents.
      max_df       : ignore terms appearing in more than max_df fraction of docs.
      ngram_range  : (1,2) captures unigrams AND bigrams e.g. "not good" as one feature.
      sublinear_tf : apply log(1+TF) to dampen the effect of high-frequency terms.
      smooth_idf   : add 1 to numerator and denominator of IDF to avoid zero division.

    Returns:
        Configured TfidfVectorizer (not yet fitted).
    """
    params = dict(
        max_features = TFIDF_MAX_FEAT,
        min_df       = TFIDF_MIN_DF,
        max_df       = TFIDF_MAX_DF,
        ngram_range  = TFIDF_NGRAM,
        sublinear_tf = True,
        smooth_idf   = True,
        strip_accents = "unicode",
    )
    params.update(kwargs)
    return TfidfVectorizer(**params)


def fit_vectorizer(texts, vectorizer: TfidfVectorizer = None) -> TfidfVectorizer:
    """
    Fit a TF-IDF vectorizer on TRAINING data only.

    IMPORTANT: Never fit on test/validation data — this causes data leakage.
               (Data Integrity)

    Args:
        texts:      Iterable of preprocessed training texts.
        vectorizer: Optional pre-created vectorizer; creates default if None.

    Returns:
        Fitted TfidfVectorizer.
    """
    if vectorizer is None:
        vectorizer = build_tfidf_vectorizer()
    vectorizer.fit(texts)
    print(f"[TF-IDF] Vocabulary size: {len(vectorizer.vocabulary_):,} features")
    return vectorizer


def transform_texts(texts, vectorizer: TfidfVectorizer):
    """
    Transform texts into TF-IDF sparse matrix using a FITTED vectorizer.

    Args:
        texts:      Iterable of text strings.
        vectorizer: Already-fitted TfidfVectorizer.

    Returns:
        scipy sparse matrix of shape (n_samples, n_features).
    """
    return vectorizer.transform(texts)


def get_top_features(vectorizer: TfidfVectorizer, X_matrix, n: int = 20) -> dict:
    """
    Extract top N features by mean TF-IDF score across the corpus.

    Feature importance in the document-term matrix.

    Args:
        vectorizer: Fitted TfidfVectorizer.
        X_matrix:   TF-IDF matrix (scipy sparse).
        n:          Number of top features to return.

    Returns:
        dict mapping feature name → mean TF-IDF score.
    """
    mean_scores = np.asarray(X_matrix.mean(axis=0)).flatten()
    feature_names = vectorizer.get_feature_names_out()
    top_idx = mean_scores.argsort()[::-1][:n]
    return {feature_names[i]: round(float(mean_scores[i]), 6) for i in top_idx}


def tfidf_math_explanation() -> str:
    """
    Return a formatted mathematical explanation of TF-IDF.
    Used in the About and Dataset Explorer pages.
    """
    return """
### TF-IDF: Term Frequency – Inverse Document Frequency

**Why do we need it?**
Machine learning models cannot process raw text. We need to convert words
into numbers. TF-IDF is a statistical measure that reflects how important
a word is to a document relative to the entire corpus.

---

**Term Frequency (TF)**

$$TF(t, d) = \\frac{\\text{count}(t \\text{ in } d)}{\\text{total terms in } d}$$

Measures how frequently a term *t* appears in document *d*.
Higher TF → the term is more prominent in that document.

---

**Inverse Document Frequency (IDF)**

$$IDF(t) = \\log\\left(\\frac{1 + N}{1 + df(t)}\\right) + 1$$

Where:
- *N* = total number of documents
- *df(t)* = number of documents containing term *t*

Words appearing in almost every document (e.g., "the", "is") get a LOW IDF.
Rare, meaningful words get a HIGH IDF.

---

**TF-IDF Score**

$$\\text{TF-IDF}(t, d) = TF(t, d) \\times IDF(t)$$

A high TF-IDF score means the term is frequent in this document
but rare across the corpus — making it a strong signal.

---

**Why Bigrams (ngram_range = (1,2))?**

Bigrams capture phrases like "not good", "very bad", "highly recommend"
which carry sentiment that single words miss. This is critical for
accurate sentiment classification.
"""


def perform_svd_analysis(X_matrix, n_components: int = 50) -> dict:
    """
    Optional: Apply TruncatedSVD (LSA) for dimensionality reduction.

    SVD, Eigenvalues, Dimensionality Reduction.
    TruncatedSVD is the sparse-matrix equivalent of PCA.
    It decomposes X ≈ U × Σ × V^T, keeping top k singular vectors.

    Args:
        X_matrix:     TF-IDF sparse matrix.
        n_components: Number of latent dimensions to keep.

    Returns:
        dict with explained_variance_ratio and cumulative variance.
    """
    svd = TruncatedSVD(n_components=n_components, random_state=RANDOM_STATE)
    svd.fit(X_matrix)
    evr = svd.explained_variance_ratio_
    return {
        "n_components":             n_components,
        "explained_variance_ratio": evr.tolist(),
        "cumulative_variance":      np.cumsum(evr).tolist(),
        "total_explained_pct":      round(float(np.sum(evr)) * 100, 2),
    }


def save_vectorizer(vectorizer: TfidfVectorizer, path: str = VECTORIZER_PATH):
    """Persist the fitted vectorizer to disk."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(vectorizer, path)
    print(f"[TF-IDF] Vectorizer saved -> {path}")


def load_vectorizer(path: str = VECTORIZER_PATH) -> TfidfVectorizer:
    """Load a previously saved vectorizer."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Vectorizer not found at: {path}")
    return joblib.load(path)

