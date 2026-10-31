# ============================================================
# src/config.py
# Global Configuration for Sentiment Analysis System
# ============================================================

import os

# ── Project Paths ─────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET_DIR     = os.path.join(BASE_DIR, "dataset")
RAW_DIR         = os.path.join(DATASET_DIR, "raw")
PROCESSED_DIR   = os.path.join(DATASET_DIR, "processed")
MODELS_DIR      = os.path.join(BASE_DIR, "models")
DATABASE_DIR    = os.path.join(BASE_DIR, "database")
NOTEBOOKS_DIR   = os.path.join(BASE_DIR, "notebooks")

# ── File Paths ────────────────────────────────────────────
RAW_CSV         = os.path.join(RAW_DIR, "sentiment_dataset.csv")
PROCESSED_CSV   = os.path.join(PROCESSED_DIR, "sentiment_processed.csv")
MODEL_PATH      = os.path.join(MODELS_DIR, "sentiment_model.pkl")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")
METADATA_PATH   = os.path.join(MODELS_DIR, "model_metadata.json")
DB_PATH         = os.path.join(DATABASE_DIR, "sentiment.db")

# ── Dataset Column Names ──────────────────────────────────
TEXT_COLUMN      = "text"
LABEL_COLUMN     = "sentiment"
TIMESTAMP_COLUMN = "timestamp"

# ── Sentiment Labels ──────────────────────────────────────
SENTIMENT_CLASSES = ["Negative", "Neutral", "Positive"]
SENTIMENT_COLORS  = {
    "Positive": "#10b981",   # emerald green
    "Negative": "#ef4444",   # red
    "Neutral":  "#6366f1",   # indigo
}

# ── Model Hyperparameters ─────────────────────────────────
RANDOM_STATE   = 42
TEST_SIZE      = 0.20
TFIDF_MAX_FEAT = 20000
TFIDF_MIN_DF   = 2
TFIDF_MAX_DF   = 0.95
TFIDF_NGRAM    = (1, 2)     # unigrams + bigrams

# ── Naive Bayes ───────────────────────────────────────────
NB_ALPHA       = 1.0         # Laplace smoothing

# ── UI ────────────────────────────────────────────────────
APP_TITLE      = "Social Media Sentiment Analysis System"
APP_ICON       = None
SIDEBAR_LOGO   = ""

# ── Ensure Directories Exist ──────────────────────────────
for _dir in [RAW_DIR, PROCESSED_DIR, MODELS_DIR, DATABASE_DIR]:
    os.makedirs(_dir, exist_ok=True)
