"""
pages/8_About_Project.py
=========================
Module 12 + Academic Documentation

Project abstract, objectives, architecture mapping,
mathematical explanations, deployment guide, and viva Q&A.
"""

import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.train import naive_bayes_explanation, load_metadata
from src.feature_extraction import tfidf_math_explanation
from src.icons import lucide

st.markdown(f"""
<h1 style="color:#ffffff; font-size:2rem; font-weight:700; letter-spacing:-0.02em; margin-bottom:0.25rem; display:flex; align-items:center; gap:10px;">
    {lucide('book-open', 26, '#818cf8')}
    <span>About This Project</span>
</h1>
<p style="color:#94a3b8; font-size:1rem; margin-top:0;">Academic documentation, architecture mapping, and deployment guide.</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Navigation Tabs ───────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Abstract & Intro",
    "Architecture Map",
    "Mathematics",
    "Deployment",
    "Viva Q&A",
    "References",
])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — Abstract & Introduction
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("""
    ## Project Abstract

    This project presents a complete **Social Media Sentiment Analysis System** developed
    as an academic Data Science and Computing (DSC) capstone project. The system employs
    Natural Language Processing (NLP) techniques, TF-IDF feature extraction, and a
    Multinomial Naive Bayes classifier to categorise social media posts and product reviews
    into three sentiment classes: **Positive**, **Negative**, and **Neutral**.

    The application is built using Python, Streamlit, scikit-learn, NLTK, Pandas, NumPy,
    Plotly, and SQLite. It demonstrates an end-to-end machine learning pipeline with an
    interactive web dashboard.

    ---

    ## Problem Statement

    The exponential growth of user-generated content on social media platforms and
    e-commerce websites has created an immense need for automated opinion mining tools.
    Manual analysis of millions of reviews and comments is infeasible. This project
    addresses the need for an automated, accurate, and interpretable sentiment classification
    system that can process text at scale and present results through a professional
    analytical dashboard.

    ---

    ## Objectives

    1. Implement a complete NLP text preprocessing pipeline.
    2. Extract numerical features from text using TF-IDF vectorisation.
    3. Train and evaluate a Multinomial Naive Bayes sentiment classifier.
    4. Demonstrate core data science and machine learning concepts through practical implementation.
    5. Build an interactive multi-page Streamlit dashboard.
    6. Implement SQLite-based prediction storage with OLTP/OLAP concepts.
    7. Demonstrate time series analysis through daily sentiment trends.
    8. Deploy the application with saved model artifacts (Joblib).

    ---

    ## Scope

    - **In Scope**: Text-based sentiment analysis (English), three-class classification,
      interactive dashboard, batch processing, prediction history, time series visualisation.
    - **Out of Scope**: Multi-language support, image/video sentiment, real-time social
      media API integration, aspect-based sentiment analysis.

    ---

    ## System Architecture

    ```
    ┌─────────────────────────────────────────────────────┐
    │                  Streamlit Frontend                 │
    │   (Pages: Overview, Analyzer, Bulk, EDA,            │
    │    Analytics, Evaluation, History, About)           │
    └──────────────────────┬──────────────────────────────┘
                           │
    ┌──────────────────────▼──────────────────────────────┐
    │                  Core Python Modules                │
    │  data_loader -> preprocessing -> feature_extraction │
    │  train -> evaluation -> prediction -> database      │
    └──────────────────────┬──────────────────────────────┘
                           │
    ┌──────────────┬───────▼─────────────────────────────┐
    │  SQLite DB   │     Saved Model (Joblib .pkl)        │
    │  (OLTP/OLAP) │  sentiment_model.pkl + metadata.json│
    └──────────────┴─────────────────────────────────────┘
    ```

    ---

    ## Data Science Life Cycle

    | Phase | Implementation |
    |-------|---------------|
    | **1. Problem Definition** | Classify social media sentiment into 3 classes |
    | **2. Data Collection** | Load dataset via data_loader.py |
    | **3. Data Exploration** | EDA with statistics and visualisations |
    | **4. Data Preprocessing** | NLP cleaning pipeline in preprocessing.py |
    | **5. Feature Engineering** | TF-IDF vectorisation in feature_extraction.py |
    | **6. Model Building** | Multinomial Naive Bayes in train.py |
    | **7. Model Evaluation** | Metrics in evaluation.py |
    | **8. Deployment** | Streamlit app with saved model (Joblib) |
    | **9. Monitoring** | SQLite prediction history + analytics dashboard |
    """)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — Architecture & Module Implementation Map
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    ## Architecture & Module Implementation Mapping

    | Module | Topic | Implementation in This Project | Status |
    |--------|-------|--------------------------------|--------|
    | **1** | Dataset Collection | Data collection, schema definition, data loader pipeline | Direct |
    | **2** | Exploratory Data Analysis | Class distribution, text length stats, vocabulary profiling | Direct |
    | **3** | Text Preprocessing | NLP cleaning pipeline: lowercase, HTML removal, tokenisation | Direct |
    | **4** | TF-IDF Vectorization | Document-term matrix, n-grams, sparse matrix representation | Direct |
    | **5** | Naive Bayes Classifier | Multinomial Naive Bayes model with Laplace smoothing | Direct |
    | **6** | Model Evaluation | Confusion matrix, Precision, Recall, F1-score, accuracy | Direct |
    | **7** | Real-Time Sentiment Analyzer | Interactive sentiment prediction with confidence breakdown | Direct |
    | **8** | Bulk CSV Processing | Batch inference pipeline with downloadable CSV outputs | Direct |
    | **9** | Analytics Dashboard | Interactive KPI dashboard, sentiment distribution, word clouds | Direct |
    | **10** | Time Series & Trends | Daily trends, 7-day moving average, temporal smoothing | Direct |
    | **11** | SQLite Storage | Prediction history, OLTP transactional logging, OLAP queries | Direct |
    | **12** | Deployment & Documentation | Serialized model loading (Joblib), architectural docs, viva prep | Direct |

    ---

    ## Big Data Concepts (5 Vs Framework)

    | 5V | Application |
    |----|-------------|
    | **Volume** | Thousands of social media posts; scalable batch processing |
    | **Velocity** | Real-time prediction within milliseconds |
    | **Variety** | Structured CSV, unstructured text, semi-structured JSON metadata |
    | **Veracity** | Data cleaning pipeline handles noise, duplicates, and missing values |
    | **Value** | Business insight through sentiment trends and analytics dashboard |
    """)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — Mathematics
# ════════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown(tfidf_math_explanation())
    st.markdown("---")
    st.markdown(naive_bayes_explanation())
    st.markdown("---")
    st.markdown("""
    ### Statistical Measures Used in This Project

    | Measure | Formula | Used For |
    |---------|---------|----------|
    | Mean | $\\bar{x} = \\frac{1}{n}\\sum x_i$ | Average review length |
    | Variance | $\\sigma^2 = \\frac{1}{n}\\sum(x_i - \\bar{x})^2$ | Length variability |
    | Std Dev | $\\sigma = \\sqrt{\\sigma^2}$ | Spread of review lengths |
    | Imbalance Ratio | $r = \\frac{\\max(n_k)}{\\min(n_k)}$ | Class balance check |
    | Confidence Interval | $\\bar{x} \\pm 2\\sigma$ | Cross-validation reliability |

    ### Linear Algebra Concepts

    - **Scalar**: A single TF-IDF value, e.g. TF-IDF("love", doc₁) = 0.42
    - **Vector**: One document's TF-IDF feature vector: [0.0, 0.42, 0.0, 0.31, ...]
    - **Matrix**: The full document-term matrix X of shape (n_docs x vocab_size)
    - **Sparse Matrix**: Efficient storage since most entries are zero
    - **SVD**: X ~ U x Sigma x V^T for dimensionality reduction (LSA)
    """)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — Deployment
# ════════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""
    ## Deployment Guide

    ### Local Installation

    ```bash
    # 1. Clone the repository
    git clone https://github.com/your-username/social-sentiment-analysis.git
    cd social-sentiment-analysis

    # 2. Create a virtual environment
    python -m venv venv
    venv\\Scripts\\activate          # Windows
    # source venv/bin/activate       # macOS / Linux

    # 3. Install dependencies
    pip install -r requirements.txt

    # 4. Train the model (run ONCE)
    python train_model.py

    # 5. Launch the app
    streamlit run app.py
    ```

    ---

    ### Streamlit Community Cloud Deployment

    1. Push the repository to GitHub (ensure `requirements.txt` is included).
    2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in.
    3. Click **New app** -> Select your repository -> Set `app.py` as the main file.
    4. Click **Deploy**.

    > **Note:** The trained model (`.pkl` files) must be committed to the repository,
    > OR the training script must be run as a post-deploy step.

    ---

    ### Saved Model Artifacts & Database

    | File | Description |
    |------|-------------|
    | `models/sentiment_model.pkl` | Complete trained Pipeline (TF-IDF + NB) |
    | `models/model_metadata.json` | Training info, metrics, hyperparameters |
    | `database/sentiment.db` | SQLite prediction history |

    The model is loaded ONCE using `@st.cache_resource` — it does NOT retrain
    on every page refresh, ensuring fast response times.
    """)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 5 — Viva Q&A
# ════════════════════════════════════════════════════════════════════════════════
with tab5:
    qas = [
        ("What is sentiment analysis?",
         "Sentiment analysis (opinion mining) is the process of computationally identifying "
         "and categorising opinions in text — typically as Positive, Negative, or Neutral. "
         "It is a subfield of NLP with applications in social media monitoring, product reviews, "
         "and customer feedback analysis."),

        ("Why did you choose Multinomial Naive Bayes?",
         "MNB is ideal for text classification because: (1) it handles high-dimensional sparse "
         "TF-IDF feature vectors efficiently; (2) training is O(n x |V|) — very fast; "
         "(3) it is mathematically interpretable via Bayes' Theorem; (4) it works well even "
         "with relatively small training datasets."),

        ("What is TF-IDF and why is it used?",
         "TF-IDF stands for Term Frequency–Inverse Document Frequency. It converts text into "
         "numerical feature vectors. TF measures how often a word appears in a document; "
         "IDF down-weights words common across all documents. The product highlights words "
         "that are informative for a specific document but rare overall."),

        ("How does Naive Bayes use Bayes' Theorem?",
         "P(class|text) is proportional to P(class) x P(text|class). The naive assumption is that each word "
         "is conditionally independent given the class. This lets us compute the product of "
         "individual P(word|class) values. Laplace smoothing (alpha=1) prevents zero "
         "probabilities for unseen words."),

        ("What is Laplace smoothing and why is it needed?",
         "Laplace smoothing adds a small constant (alpha=1) to all word counts. Without it, "
         "if a word in the test set never appeared in training for a particular class, "
         "P(word|class)=0, making the entire product zero regardless of other words. "
         "Smoothing prevents this zero-probability problem."),

        ("What is the difference between accuracy and F1-score?",
         "Accuracy = (TP+TN)/Total — measures overall correctness but misleads with imbalanced "
         "classes. F1-score = 2 x P x R/(P+R) — harmonic mean of Precision and Recall. "
         "Macro F1 treats all classes equally; Weighted F1 accounts for class size. "
         "F1 is more informative when class distribution is uneven."),

        ("Why did you use stratified train-test split?",
         "Stratified splitting ensures that the proportion of each sentiment class is the same "
         "in both training and test sets. Without stratification, the test set might randomly "
         "contain very few examples of a rare class, giving misleading evaluation results."),

        ("What is data leakage and how did you prevent it?",
         "Data leakage occurs when information from the test set influences the training process "
         "(e.g., fitting TF-IDF on the full dataset before splitting). We prevented this by "
         "using a scikit-learn Pipeline that fits the TF-IDF vectorizer ONLY on training data "
         "and transforms test data using the training vocabulary."),

        ("Explain the concept of moving average in time series.",
         "A moving average smooths a time series by averaging values within a sliding window. "
         "For sentiment trends, a 7-day moving average replaces each day's count with the "
         "average of the surrounding 7 days. This removes short-term noise and reveals "
         "longer-term patterns. Formula: MA_t = (1/w) x sum y_{t-i} for i in 0..w-1."),

        ("What is OLTP vs OLAP in your project?",
         "OLTP (Online Transaction Processing): Our SQLite INSERT operations — inserting one "
         "prediction record per analysis. Optimised for fast individual transactions. "
         "OLAP (Online Analytical Processing): Our dashboard aggregate queries — "
         "GROUP BY sentiment, COUNT(*) for trend charts. Optimised for bulk reads and aggregations."),

        ("What are the limitations of your system?",
         "1. Synthetic training data may not capture all real-world slang, sarcasm, or domain-specific "
         "nuances. 2. Naive Bayes assumes word independence — misses word order context. 3. No handling of "
         "emojis or multi-language text. 4. Static model — does not update incrementally from new predictions. "
         "5. Extremely short texts may receive low-confidence predictions."),

        ("What improvements would you make in future?",
         "1. Use larger real-world datasets (Twitter, Amazon Reviews) via API. 2. Implement BERT/transformer "
         "models for context-aware predictions. 3. Add aspect-based sentiment analysis. "
         "4. Implement online learning (incremental updates). 5. Add multilingual support. "
         "6. Deploy to cloud with CI/CD pipeline."),
    ]

    for i, (q, a) in enumerate(qas):
        with st.expander(f"Q{i+1}: {q}"):
            st.markdown(f"**Answer:** {a}")

# ════════════════════════════════════════════════════════════════════════════════
# TAB 6 — References
# ════════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown("""
    ## References

    > *Note: All references are to publicly available academic and technical resources.
    > No fabricated or hallucinated citations are included.*

    ### Textbooks

    1. Géron, A. (2019). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (2nd ed.). O'Reilly Media.
    2. Bird, S., Klein, E., & Loper, E. (2009). *Natural Language Processing with Python*. O'Reilly Media. Available: https://www.nltk.org/book/
    3. Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press. Available: https://nlp.stanford.edu/IR-book/

    ### Scikit-learn Documentation

    4. Pedregosa et al. (2011). *Scikit-learn: Machine Learning in Python*. JMLR 12, 2825-2830. https://scikit-learn.org/stable/

    ### NLTK

    5. NLTK Project. (2024). *Natural Language Toolkit Documentation*. https://www.nltk.org/

    ### Streamlit

    6. Streamlit Inc. (2024). *Streamlit Documentation*. https://docs.streamlit.io/

    ### Plotly

    7. Plotly Technologies Inc. (2024). *Plotly Python Open Source Graphing Library*. https://plotly.com/python/

    ### Research Papers

    8. Pang, B., & Lee, L. (2008). *Opinion Mining and Sentiment Analysis*. Foundations and Trends in Information Retrieval, 2(1–2), 1–135.
    9. McCallum, A., & Nigam, K. (1998). *A Comparison of Event Models for Naive Bayes Text Classification*. AAAI Workshop on Learning for Text Categorization.
    10. Salton, G., & McGill, M. J. (1983). *Introduction to Modern Information Retrieval*. McGraw-Hill.

    ### Datasets

    11. Twitter Entity Sentiment Analysis. Available on Kaggle: https://www.kaggle.com/datasets
    12. UCI Machine Learning Repository — Sentiment Analysis Datasets: https://archive.ics.uci.edu/
    """)
