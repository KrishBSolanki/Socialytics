"""
app.py
======
Main Streamlit Entry Point — Social Media Sentiment Analysis System
Uses st.navigation for seamless, instant page routing without full page reloads.
"""

import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import APP_ICON, APP_TITLE
from src.database import init_db
from src.icons import lucide
from src.styles import apply_custom_styles

# ── App-wide Page Configuration ───────────────────────────────
st.set_page_config(
    page_title = APP_TITLE,
    page_icon  = APP_ICON,
    layout     = "wide",
    initial_sidebar_state = "expanded",
)

# ── Inject styles and scripts ONCE globally ───────────────────
apply_custom_styles()
init_db()

# ── Sidebar Brand Header: DISPLAYED AT THE VERY TOP ───────────
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-brand-header">
        {lucide('brain', 24, '#818cf8')}
        <span style="font-size:1.2rem; font-weight:700; color:#f8fafc; letter-spacing:-0.01em;">Sentiment AI</span>
    </div>
    """, unsafe_allow_html=True)

# ── Multi-Page Navigation ─────────────────────────────────────
pages = [
    st.Page("pages/1_Overview.py",           title="Overview",              url_path="Overview",             default=True),
    st.Page("pages/2_Sentiment_Analyzer.py", title="Sentiment Analyzer",     url_path="Sentiment_Analyzer"),
    st.Page("pages/3_Bulk_Analysis.py",      title="Bulk Analysis",          url_path="Bulk_Analysis"),
    st.Page("pages/4_Dataset_Explorer.py",   title="Dataset Explorer",       url_path="Dataset_Explorer"),
    st.Page("pages/5_Analytics.py",          title="Analytics Dashboard",    url_path="Analytics"),
    st.Page("pages/6_Model_Evaluation.py",   title="Model Evaluation",       url_path="Model_Evaluation"),
    st.Page("pages/7_Prediction_History.py", title="Prediction History",     url_path="Prediction_History"),
    st.Page("pages/8_About_Project.py",      title="About Project",          url_path="About_Project"),
]

pg = st.navigation(pages, position="sidebar")
pg.run()
