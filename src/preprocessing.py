"""
src/preprocessing.py
====================
Module 3 – Text Preprocessing Pipeline

Steps:
  1. Lowercase conversion
  2. HTML tag removal
  3. URL removal
  4. Special character / punctuation removal
  5. Extra whitespace removal
  6. Tokenization
  7. Stopword removal (preserving negations)
  8. Missing value handling
  9. Duplicate removal

Data Transformation and Data Integrity
Tokenization as a vector-space operation
"""

import re
import string
import unicodedata
from typing import List, Optional

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from src.config import TEXT_COLUMN, LABEL_COLUMN, RANDOM_STATE


# ── Download required NLTK resources (one-time) ──────────────────────────────
def _download_nltk_resources():
    """
    Download NLTK corpora if not already present.
    Silently skips on network failure — app degrades gracefully.
    """
    resources = [
        ("tokenizers/punkt_tab",  "punkt_tab"),
        ("tokenizers/punkt",      "punkt"),
        ("corpora/stopwords",     "stopwords"),
    ]
    for path, name in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            try:
                nltk.download(name, quiet=True)
            except Exception:
                pass  # offline / no network — handled below

try:
    _download_nltk_resources()
except Exception:
    pass


# ── Negation words to PRESERVE (not remove as stopwords) ─────────────────────
# DSC best practice: Removing "not", "no", "never" destroys sentiment signal
NEGATION_WORDS = {
    "not", "no", "never", "nor", "neither", "nobody", "nothing",
    "nowhere", "hardly", "scarcely", "barely", "without", "don't",
    "doesn't", "didn't", "won't", "wouldn't", "can't", "cannot",
    "couldn't", "shouldn't", "isn't", "aren't", "wasn't", "weren't",
}

# Build custom stopword list that preserves negations
try:
    _raw_stopwords = set(stopwords.words("english"))
except LookupError:
    # Fallback minimal stopword list if corpus not available
    _raw_stopwords = {
        "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
        "your", "yours", "he", "him", "his", "she", "her", "it", "its",
        "they", "them", "their", "what", "which", "who", "whom", "this",
        "that", "these", "those", "am", "is", "are", "was", "were", "be",
        "been", "being", "have", "has", "had", "do", "does", "did",
        "will", "would", "shall", "should", "may", "might", "must", "can",
        "could", "ought", "a", "an", "the", "and", "but", "or", "for",
        "of", "in", "to", "at", "by", "as", "on", "with", "from",
    }
CUSTOM_STOPWORDS = _raw_stopwords - NEGATION_WORDS

# Compile regex patterns once for efficiency
_RE_HTML    = re.compile(r"<[^>]+>")
_RE_URL     = re.compile(r"https?://\S+|www\.\S+")
_RE_EMAIL   = re.compile(r"\S+@\S+\.\S+")
_RE_MENTION = re.compile(r"@\w+")
_RE_HASHTAG = re.compile(r"#(\w+)")          # keep word, remove #
_RE_NUMBERS = re.compile(r"\b\d+\b")
_RE_SPACE   = re.compile(r"\s+")
_RE_PUNCT   = re.compile(r"[^\w\s]")


# ── Core cleaning function ────────────────────────────────────────────────────
def clean_text(text: str, remove_stopwords: bool = True) -> str:
    """
    Apply full NLP preprocessing pipeline to a single text string.

    Args:
        text:             Raw input text.
        remove_stopwords: Whether to remove stopwords (preserving negations).

    Returns:
        Cleaned, normalised text string.
    """
    if not isinstance(text, str) or not text.strip():
        return ""

    # Step 1 – Unicode normalisation (handles smart quotes, accents, etc.)
    text = unicodedata.normalize("NFKD", text)

    # Step 2 – Lowercase
    text = text.lower()

    # Step 3 – Remove HTML tags
    text = _RE_HTML.sub(" ", text)

    # Step 4 – Remove URLs
    text = _RE_URL.sub(" ", text)

    # Step 5 – Remove email addresses
    text = _RE_EMAIL.sub(" ", text)

    # Step 6 – Remove @mentions (social media)
    text = _RE_MENTION.sub(" ", text)

    # Step 7 – Expand hashtags (keep the word, remove #)
    text = _RE_HASHTAG.sub(r"\1", text)

    # Step 8 – Remove standalone numbers (keep alpha-numerics in words)
    text = _RE_NUMBERS.sub(" ", text)

    # Step 9 – Remove punctuation
    text = _RE_PUNCT.sub(" ", text)

    # Step 10 – Collapse extra whitespace
    text = _RE_SPACE.sub(" ", text).strip()

    # Step 11 – Tokenize
    # Tokenize — fall back to simple split if NLTK punkt not available
    try:
        tokens: List[str] = word_tokenize(text)
    except LookupError:
        tokens = text.split()

    # Step 12 – Remove stopwords (preserving negation words)
    if remove_stopwords:
        tokens = [t for t in tokens if t not in CUSTOM_STOPWORDS]

    # Step 13 – Remove very short tokens (length < 2)
    tokens = [t for t in tokens if len(t) >= 2]

    return " ".join(tokens)


def preprocess_dataframe(
    df: pd.DataFrame,
    text_col: str = TEXT_COLUMN,
    remove_duplicates: bool = True,
    remove_empty: bool = True,
) -> pd.DataFrame:
    """
    Apply preprocessing to an entire DataFrame.

    Adds a 'clean_text' column while preserving the original text.
    Missing values → duplicate removal → transformation.

    Args:
        df:                The input DataFrame.
        text_col:          Name of the column containing raw text.
        remove_duplicates: Drop duplicate rows based on raw text.
        remove_empty:      Drop rows where cleaned text is empty.

    Returns:
        Preprocessed DataFrame with new 'clean_text' column.
    """
    df = df.copy()

    # ── Handle missing text values ────────────────────────────────────────
    n_missing = df[text_col].isnull().sum()
    if n_missing > 0:
        print(f"[Preprocess] Dropping {n_missing} rows with missing text.")
        df = df.dropna(subset=[text_col])

    # ── Remove duplicates ─────────────────────────────────────────────────
    if remove_duplicates:
        n_before = len(df)
        df = df.drop_duplicates(subset=[text_col])
        n_dupes = n_before - len(df)
        if n_dupes > 0:
            print(f"[Preprocess] Removed {n_dupes} duplicate records.")

    # ── Apply clean_text to each row ──────────────────────────────────────
    df["clean_text"] = df[text_col].apply(clean_text)

    # ── Drop rows where cleaning produces empty string ────────────────────
    if remove_empty:
        n_before = len(df)
        df = df[df["clean_text"].str.strip().str.len() > 0]
        n_empty = n_before - len(df)
        if n_empty > 0:
            print(f"[Preprocess] Removed {n_empty} rows with empty cleaned text.")

    df = df.reset_index(drop=True)
    print(f"[Preprocess] Final dataset size: {len(df):,} records.")
    return df


def get_preprocessing_stats(df_raw: pd.DataFrame, df_clean: pd.DataFrame) -> dict:
    """
    Compute before/after statistics for preprocessing report.

    Data transformation audit.
    """
    stats = {
        "raw_records":        len(df_raw),
        "clean_records":      len(df_clean),
        "records_removed":    len(df_raw) - len(df_clean),
        "removal_pct":        round((len(df_raw) - len(df_clean)) / len(df_raw) * 100, 2),
        "avg_raw_length":     round(df_raw[TEXT_COLUMN].dropna().str.len().mean(), 2),
        "avg_clean_length":   round(df_clean["clean_text"].str.len().mean(), 2),
        "vocab_raw":          df_raw[TEXT_COLUMN].dropna().str.lower()
                                  .str.split().explode().nunique(),
        "vocab_clean":        df_clean["clean_text"].str.split().explode().nunique(),
    }
    return stats

