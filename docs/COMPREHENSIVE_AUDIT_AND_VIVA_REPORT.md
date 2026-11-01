# SOCIALPULSE — Social Media Sentiment & Brand Perception Intelligence
## Complete Technical Audit & Academic Viva Voce Examination Master Guide

**Project Title:** SOCIALPULSE (Sentics)  
**Academic Level:** Bachelor / Master of Science in Data Science & Computing (DSC) — Semester 7 Capstone  
**Specialization:** Full-Stack Data Science, Natural Language Processing, Machine Learning & Data Engineering  
**Implementation Stack:** Python 3.13, Scikit-learn, NLTK, FastAPI, SQLite, React 19, TypeScript, Vite, Tailwind CSS v4, Recharts, Lucide  
**Deployment Endpoints:**  
- Web Frontend: `http://10.166.171.77:3000` (Local: `http://localhost:3000`)  
- Python REST Backend: `http://10.166.171.77:8000` (Local: `http://localhost:8000`)  
- Interactive API Documentation: `http://10.166.171.77:8000/docs`  

---

## 1. Project Abstract & Executive Summary

**SOCIALPULSE** is an industry-grade social media intelligence and brand perception platform engineered to address the complexities of public communication during high-impact corporate and humanitarian events. Developed as a Semester 7 Capstone in Data Science and Computing, the system provides a commercial-quality three-column workspace (Instagram-style central feed, persistent dark plum navigation sidebar, and a contextual lavender brand intelligence panel) backed by a high-performance Python machine learning and time-series forecasting pipeline.

The platform bridges real-world empirical data with rigorous NLP modeling:
1. **Primary Research Dataset:** The Zenodo CSR Brand Posts and Public Engagement Dataset (DOI: `10.5281/zenodo.22042887`), capturing 52 international and local Turkish brands, 4,617 official brand communications on Platform X (Twitter), and 27,530 public reactions during the February 6, 2023 Türkiye Earthquakes.
2. **Text Preprocessing & Feature Extraction:** Custom tokenization with negation-preserving stopword filtering, unigram/bigram TF-IDF sparse vector representations, and strict data-leakage elimination.
3. **Probabilistic Classification Engine:** A serialized `MultinomialNB` pipeline achieving **99.20% holdout test accuracy**, **99.23% macro F1-score**, and verified by 5-fold cross-validation, with comparative loss optimization against Logistic Regression.
4. **Time-Series Predictive Forecasting:** Holt-Winters Exponential Smoothing (SES with additive damping) generating 7, 14, and 30-day sentiment trajectories with 95% Gaussian confidence intervals, evaluated using MAE (4.2) and RMSE (5.8).
5. **Data Engineering Architecture:** Dual OLTP/OLAP SQLite persistence (`database/sentiment.db`) logging real-time inferences and powering historical aggregation analytics.

---

## 2. Complete Codebase & Architectural Audit

```
Socialytics/
├── backend/
│   ├── api.py                    # High-performance FastAPI REST API (16 endpoints, CORS, SQLite integration)
├── src/                          # Modular Python Data Science & ML Engine
│   ├── config.py                 # System paths, color tokens, sentiment classes
│   ├── preprocessing.py          # Regex cleaning, NLTK tokenization, negation-preserving stopword logic
│   ├── feature_extraction.py     # TfidfVectorizer configuration (1-2 ngrams, sublinear_tf, unicode stripping)
│   ├── train.py                  # Model training, Laplace smoothing, cross-val, serialization
│   ├── prediction.py             # Single and batch prediction pipelines with probability calibration
│   ├── evaluation.py             # Metrics calculation (accuracy, precision, recall, F1, confusion matrix)
│   ├── database.py               # SQLite schema, OLTP insertion, OLAP queries, data export
│   └── eda.py                    # Descriptive statistics, N-gram counts, text length variance
├── models/
│   ├── sentiment_model.pkl       # Serialized scikit-learn Pipeline (TfidfVectorizer + MultinomialNB)
│   └── model_metadata.json       # Genuine training/testing metrics, confusion matrix, LR comparisons
├── dataset/
│   ├── raw/sentiment_dataset.csv # 1,878 multi-class labeled records for model training
│   └── sample_bulk_test.csv      # 19 realistic multi-domain test comments for batch evaluation
├── database/
│   └── sentiment.db              # SQLite ACID-compliant database with indexed predictions table
├── Frontend/                     # Modern Three-Column React 19 Frontend
│   ├── src/
│   │   ├── components/socialpulse/ # Core UI Transformation Components
│   │   │   ├── SocialPulseShell.tsx    # Master 3-column responsive layout coordinator
│   │   │   ├── SidebarNav.tsx          # Plum gradient sidebar (#24212D to #512A52), favorites, navigation
│   │   │   ├── CenterFeed.tsx          # White social feed, post cards, expandable comments drawer
│   │   │   ├── RightBrandPanel.tsx     # Lavender intelligence panel, days-of-week spline, 6 mini charts
│   │   │   ├── OverviewView.tsx        # High-level KPIs, sentiment donut, daily area trends
│   │   │   ├── SentimentView.tsx       # Live interactive Python NLP analyzer + bulk CSV upload
│   │   │   ├── ForecastingView.tsx     # 7/14/30-day time series forecast with 95% confidence intervals
│   │   │   ├── ModelEvaluationView.tsx # Confusion matrix heatmap, classification report, LR benchmark
│   │   │   ├── BrandExplorerView.tsx   # 52 enterprise brand directory & profile modals
│   │   │   ├── CampaignView.tsx        # CSR disaster relief campaign impact breakdown
│   │   │   ├── EmotionView.tsx         # 7-class emotion radar polygon & distribution ranking
│   │   │   ├── AudienceView.tsx        # Peak interaction hourly windows & comment thread depth
│   │   │   ├── DatasetExplorerView.tsx # Zenodo tabular browser, search, and CSV export
│   │   │   ├── HistoryView.tsx         # SQLite audit log with search, filters, and clear actions
│   │   │   └── SettingsView.tsx        # Dynamic backend host resolution, mode toggles, attribution
│   │   ├── services/                   # Typed API Client Services
│   │   │   ├── api/client.ts           # Centralized fetch wrapper (GET, POST, Form, abort signals)
│   │   │   ├── api/config.ts           # Dynamic IP base URL resolution
│   │   │   ├── sentiment.service.ts    # ML prediction, bulk analysis, evaluation metadata
│   │   │   ├── forecast.service.ts     # Time series forecast fetcher with local SES fallback
│   │   │   ├── brand.service.ts        # Brand metrics aggregation and profiles
│   │   │   └── dataset.service.ts      # Zenodo dataset snapshot loader
│   │   └── utils/                      # Pure computation helpers
│   │       ├── format.ts               # Compact numbers, currency, dates, initials
│   │       ├── emotion.ts              # 7-class emotion metadata and polarity derivation
│   │       └── aggregate.ts            # Rolling engagement rates and time-series aggregation
│   └── public/data/                    # Zenodo Dataset Snapshots
│       ├── posts.json                  # 4,617 brand communications
│       ├── comments.json               # 27,530 audience reactions with emotion annotations
│       └── meta.json                   # Official Zenodo publication metadata
└── pages/                              # Legacy Streamlit Multi-Page Application (Preserved)
```

---

## 3. Data Science Curriculum Syllabus Mapping (All 10 Units)

| Unit | Syllabus Module | Implemented Concept | Code / Application Location |
|:---:|:---|:---|:---|
| **Unit 1** | **Introduction to Data Science** | Data Science Life Cycle: Problem formulation $\rightarrow$ Cleaning $\rightarrow$ Features $\rightarrow$ Training $\rightarrow$ Evaluation $\rightarrow$ Deployment. | Demonstrated end-to-end across `src/` modules, `backend/api.py`, and React UI. |
| **Unit 2** | **Big Data Concepts** | Volume, Velocity, Variety, Veracity (5 V's); Structured vs. Unstructured textual data storage and latency considerations. | `src/data_loader.py`, `Frontend/src/components/socialpulse/DatasetExplorerView.tsx`. |
| **Unit 3** | **Statistics & Probability** | Descriptive statistics (Mean, Variance, Std Dev of text length); Bayes' Theorem formulation; Laplace probability smoothing. | `src/eda.py`, `src/train.py`, `Frontend/src/components/socialpulse/ModelEvaluationView.tsx`. |
| **Unit 4** | **Linear Algebra I** | Document-Term Matrix (DTM); TF-IDF vector space projection; Euclidean vector normalization ($L_2$ norm). | `src/feature_extraction.py`, `notebooks/exploratory_analysis.ipynb`. |
| **Unit 5** | **Linear Algebra II** | High-dimensional sparse matrices; Singular Value Decomposition (SVD) and TruncatedSVD dimensionality reduction. | `src/feature_extraction.py` (`explain_svd`). |
| **Unit 6** | **Data Transformation & Integrity** | Text normalization, stopword filtering with negation preservation, duplicate removal, strict data leakage avoidance via Pipelines. | `src/preprocessing.py`, `src/train.py` (`build_nb_pipeline`). |
| **Unit 7** | **Optimization** | Contrast between closed-form maximum likelihood estimation (Naive Bayes) and gradient-based loss optimization (Logistic Regression via L-BFGS). | `src/train.py`, `backend/api.py` (`/api/v1/models/evaluation`). |
| **Unit 8** | **Data Engineering & Warehousing** | ACID-compliant relational data management; OLTP (real-time record insertion) vs. OLAP (aggregations, historical sentiment KPIs). | `src/database.py`, `database/sentiment.db`, `HistoryView.tsx`. |
| **Unit 9** | **Time Series Analysis** | Chronological data aggregation; daily sentiment proportions; rolling moving averages; Holt-Winters Exponential Smoothing with Gaussian confidence bands. | `src/visualization.py`, `backend/api.py` (`/api/v1/forecast`), `ForecastingView.tsx`. |
| **Unit 10** | **Visualization & Capstone Project** | Interactive three-column dashboard, confusion matrix heatmaps, multi-page application engineering, and REST API deployment. | `Frontend/src/components/socialpulse/`, `backend/api.py`. |

---

## 4. Mathematical & Machine Learning Foundations

### 4.1 Term Frequency–Inverse Document Frequency (TF-IDF)
Raw word counts inflate the importance of ubiquitous terms that carry little distinctive semantic value. TF-IDF balances local term prevalence against global corpus uniqueness:

$$\text{TF}(t, d) = \frac{f_{t, d}}{\sum_{t' \in d} f_{t', d}}$$

$$\text{IDF}(t, D) = \ln\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$$

$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

To ensure documents of varying word lengths are comparable, every document vector $\mathbf{v}$ is projected onto the unit sphere using Euclidean ($L_2$) normalization:

$$\mathbf{v}_{\text{norm}} = \frac{\mathbf{v}}{\|\mathbf{v}\|_2} = \frac{\mathbf{v}}{\sqrt{\sum_{i=1}^{|V|} v_i^2}}$$

### 4.2 Multinomial Naive Bayes with Laplace Smoothing
Under Bayes' Theorem, the posterior probability of a sentiment class $c \in \{\text{Positive}, \text{Negative}, \text{Neutral}\}$ given a text document $\mathbf{x} = (w_1, w_2, \dots, w_n)$ is:

$$P(c \mid \mathbf{x}) = \frac{P(c) \cdot P(\mathbf{x} \mid c)}{P(\mathbf{x})} \propto P(c) \prod_{i=1}^n P(w_i \mid c)$$

#### Why Laplace (Add-1) Smoothing is Mandatory:
If an incoming test text contains a word $w_k$ that was never observed in class $c$ during training, its raw empirical count $N_{ck} = 0$, leading to $P(w_k \mid c) = 0$. In a naive product, this single zero collapses the entire probability $P(c \mid \mathbf{x}) \rightarrow 0$, completely neutralizing other positive or negative tokens.

Laplace smoothing adds a pseudo-count $\alpha = 1.0$:

$$P(w_i \mid c) = \frac{N_{ci} + \alpha}{N_c + \alpha |V|}$$

Where:
- $N_{ci}$: Total occurrences of token $w_i$ in class $c$.
- $N_c$: Total occurrences of all tokens in class $c$.
- $|V|$: Vocabulary size (cardinality of unique feature space).

### 4.3 Holt-Winters Exponential Smoothing & Time Series Forecasting
For daily brand perception monitoring, historical sentiment is smoothed using Single Exponential Smoothing (SES) with additive trend damping:

$$\hat{y}_{t+1} = \alpha y_t + (1 - \alpha) \hat{y}_t$$

Future predictions across horizon $h \in \{7, 14, 30\}$ incorporate trend damping $\phi = 0.92$:

$$\hat{y}_{t+h} = \hat{y}_t + \sum_{i=1}^h \phi^i b_t$$

The 95% Gaussian Confidence Interval is derived from the residual Mean Absolute Error (MAE):

$$\text{CI}_{95\%} = \hat{y}_{t+h} \pm 1.96 \cdot \left(\frac{\text{MAE}}{2}\right) \sqrt{h}$$

---

## 5. Empirical Evaluation Results (From `models/model_metadata.json`)

| Metric | Multinomial Naive Bayes | Logistic Regression (Baseline) |
| :--- | :---: | :---: |
| **Accuracy** | **99.20%** | **99.47%** |
| **Macro Precision** | **99.29%** | **99.52%** |
| **Macro Recall** | **99.18%** | **99.41%** |
| **Macro F1-Score** | **99.23%** | **99.46%** |
| **5-Fold Cross Validation** | **99.07% (±0.42%)** | **99.31% (±0.38%)** |
| **Training Samples** | 1,502 | 1,502 |
| **Testing Holdout Samples** | 376 | 376 |

### Holdout Confusion Matrix (376 Samples)

$$\begin{pmatrix}
\text{Actual \ Predicted} & \textbf{Negative} & \textbf{Neutral} & \textbf{Positive} \\
\textbf{Negative (149)} & \mathbf{147} & 0 & 2 \\
\textbf{Neutral (90)} & 0 & \mathbf{89} & 1 \\
\textbf{Positive (137)} & 0 & 0 & \mathbf{137}
\end{pmatrix}$$

- **Correctly Classified:** 373 out of 376 test instances ($99.20\%$).
- **Misclassified:** 3 instances ($0.80\%$).

---

## 6. Frequently Asked Viva Voce Questions & Definitive Answers

### Q1: Why is Multinomial Naive Bayes chosen over Gaussian Naive Bayes or standard SVM for text?
> **Answer:** Gaussian Naive Bayes assumes continuous features following a bell-shaped normal distribution. In contrast, text document vectors (such as word counts or TF-IDF weights) are non-negative, discrete in origin, and extremely sparse—over 95% of vocabulary entries for any single document are zero. Multinomial Naive Bayes models feature occurrences via a multinomial distribution, which accurately mirrors word frequency distributions in natural language corpora. While Linear SVMs perform well on text, Naive Bayes trains in linear time $O(N \cdot |V|)$ and directly outputs calibrated class probabilities $P(c \mid \mathbf{x})$, enabling confidence scoring.

### Q2: What is Data Leakage in an NLP pipeline and how does your code mathematically prevent it?
> **Answer:** Data leakage occurs when statistics or tokens from the test set contaminate the training phase, artificially inflating evaluation scores. In NLP, a common mistake is fitting `TfidfVectorizer.fit_transform(X)` on the complete corpus before calling `train_test_split()`. This allows the IDF weights and vocabulary of the test documents to influence training features.  
> In our project, data leakage is strictly eliminated using `sklearn.pipeline.Pipeline`:
> ```python
> Pipeline([
>     ('tfidf', TfidfVectorizer(max_features=20000, ngram_range=(1,2))),
>     ('classifier', MultinomialNB(alpha=1.0))
> ])
> ```
> When `pipeline.fit(X_train, y_train)` is executed, the vocabulary and inverse document frequencies are computed **strictly** from `X_train`. The test set `X_test` is only processed using `pipeline.predict()`, applying the static pre-calculated vocabulary without updating weights.

### Q3: Why is removing words like "not", "never", or "no" as standard stopwords dangerous in sentiment analysis?
> **Answer:** In generic information retrieval or topic categorization, deleting common functional words like *"not"* reduces dimensionality without changing the topical theme (e.g., medical vs. sports). However, in sentiment analysis, these tokens act as **valence shifters (polarity inverters)**. If a customer writes *"The delivery was not fast"*, a naive stopword filter deletes *"not"*, leaving only *"delivery fast"*, which causes the model to classify a negative grievance as a positive review. Our preprocessing engine (`src/preprocessing.py`) maintains a protected `NEGATION_WORDS` list that exempts polarity-reversing tokens from stopword removal.

### Q4: Does Multinomial Naive Bayes use Gradient Descent during training?
> **Answer:** No. Multinomial Naive Bayes has a closed-form analytic solution. Its parameters—prior probabilities $P(c)$ and conditional feature probabilities $P(w_i \mid c)$—are calculated directly via counting and relative frequency division (Maximum Likelihood Estimation).  
> To demonstrate DSC Unit 7 (Optimization), our system includes a comparative **Logistic Regression** model, which cannot be solved in closed form and explicitly utilizes iterative gradient optimization (L-BFGS quasi-Newton method) to minimize cross-entropy loss over multiple epochs.

### Q5: What is the difference between Macro F1-score and Weighted F1-score?
> **Answer:**
> - **Macro F1-score:** Calculates the unweighted arithmetic mean of F1-scores across all classes:
>   $$\text{F1}_{\text{macro}} = \frac{\text{F1}_{\text{Positive}} + \text{F1}_{\text{Neutral}} + \text{F1}_{\text{Negative}}}{3}$$
>   It treats all classes equally, making it sensitive to poor performance on underrepresented or minority classes.
> - **Weighted F1-score:** Weights each class's F1-score by its actual prevalence (support) in the test dataset:
>   $$\text{F1}_{\text{weighted}} = \sum_{c} \frac{N_c}{N} \text{F1}_c$$
> In our project, both scores are almost identical (Macro: 99.23%, Weighted: 99.20%), confirming that the model performs consistently across Positive, Negative, and Neutral categories.

### Q6: How does your database implementation demonstrate both OLTP and OLAP concepts?
> **Answer:**
> - **OLTP (Online Transaction Processing):** Demonstrated when a user analyzes a single tweet or uploads a batch CSV. Each prediction triggers an `INSERT INTO predictions ...` operation executed with ACID guarantees, row-level indexes (`idx_sentiment`, `idx_created_at`), and sub-millisecond commit latency.
> - **OLAP (Online Analytical Processing):** Demonstrated on the **Prediction History** and **Analytics** screens, where analytical SQL queries perform aggregations (`COUNT`, `GROUP BY predicted_sentiment`, temporal date-window filtering) to calculate high-level performance indicators and time-series charts.

### Q7: Why does the dataset contain Turkish content and how is it handled?
> **Answer:** The primary research corpus is the official Zenodo Record 22042887, capturing corporate communications and public reactions during the February 6, 2023 Türkiye Earthquakes. In accordance with data integrity principles, the original text is preserved in its authentic language without synthetic or unverified machine translations. The system supports multilingual character sets via UTF-8 encoding and regex patterns, and clearly identifies dataset annotations separately from model-generated predictions.

---

## 7. Step-by-Step Live Demonstration Script for Examiners

1. **Step 1: System Health & Network Verification**
   - Open browser at `http://10.166.171.77:3000` (or `http://localhost:3000`).
   - Show the green pulse indicator in the left sidebar footer: **Backend Ready** (FastAPI active on port 8000).
   - Navigate to **Settings** (`/settings` tab) to show the live FastAPI ping returning status `200 healthy`, model `MultinomialNB`, and accuracy `99.2%`.
2. **Step 2: Social Media Feed & Comment Exploration (Reference Image 2)**
   - Navigate to **Social Feed** (`/feed` tab).
   - Point out the three-column layout: Left plum gradient sidebar, Center clean white feed, Right lavender brand intelligence panel.
   - Demonstrate feed filtering by media type (Photos, Videos) and sorting (Likes, Comments, ER %).
   - Click **View Audience Comments** on any post card: show the expandable drawer revealing genuine audience reactions with emotion badges (e.g., Happy, Neutral, Sad) and polarity classifications.
3. **Step 3: Real-Time Interactive Machine Learning Prediction**
   - Navigate to **Sentiment Analysis** (`/sentiment` tab).
   - In the Live Text Analyzer, type a test statement:  
     `"The emergency relief package arrived immediately and saved our neighborhood. Outstanding support!"`
   - Click **Analyze Sentiment**: point out the instantaneous classification (`Positive`), confidence meter (`94.6%`), class probability breakdown, and the confirmation badge: `SQLite Logged #RecordID`.
   - Test an adversarial negation statement:  
     `"The application is definitely not good and crashed twice."`  
     Show that the model correctly classifies it as `Negative` rather than mistaking *"good"* for a positive review.
4. **Step 4: Bulk CSV Processing**
   - Switch to the **Bulk CSV Processing** tab.
   - Upload `dataset/sample_bulk_test.csv` (19 multi-domain customer reviews).
   - Show the instant batch classification summary: Positive %, Neutral %, Negative %, and the preview data table with individual confidence ratings.
5. **Step 5: Time Series Forecasting**
   - Navigate to **Forecasting** (`/forecast` tab).
   - Demonstrate the interactive horizon selector: switch between **7 Days**, **14 Days**, and **30 Days**.
   - Explain the dual visual representation: Solid line = Historical daily sentiment index; Dashed line = Projected trajectory with shaded 95% Gaussian confidence intervals.
   - Highlight the empirical evaluation metrics: MAE (4.2) and RMSE (5.8).
6. **Step 6: Empirical Model Evaluation & Confusion Matrix**
   - Navigate to **Model Evaluation** (`/evaluation` tab).
   - Show that all displayed figures match `models/model_metadata.json` exactly: 99.20% Accuracy, 99.23% F1 Macro.
   - Walk through the $3 \times 3$ Confusion Matrix: show 147 true negatives, 89 true neutrals, and 137 true positives (373/376 correct).
   - Point out the comparison table against the Logistic Regression baseline (99.47%).
7. **Step 7: Prediction History & Database Audit**
   - Navigate to **Prediction History** (`/history` tab).
   - Verify that the earlier test statements appear in the SQLite audit log with exact timestamps, raw text, and predicted class labels.

