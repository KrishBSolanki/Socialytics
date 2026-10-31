"""
src/styles.py
=============
Centralised styling, custom CSS, Google Fonts (Lato, Material Symbols),
and Lucide icons script for the Social Media Sentiment Analysis System.
"""

from src.icons import LUCIDE_CDN

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

/* ── Base App & Background ─────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"], .main {
    background-color: #0d0d1a !important;
    color: #e2e8f0 !important;
}

.block-container {
    padding: 1.5rem 2rem 3rem !important;
    max-width: 100% !important;
}

/* ── Typography (Lato) ─────────────────────────────────────── */
html, body, p, h1, h2, h3, h4, h5, h6, label, input, textarea, .stMarkdown,
[data-testid="stMetricValue"], [data-testid="stMetricLabel"],
div[data-testid="metric-container"], .card, .stSelectbox, .stMultiSelect {
    font-family: 'Lato', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
}

div.stButton > button {
    font-family: 'Lato', sans-serif !important;
}

/* ── Streamlit Material Symbols Protection ─────────────────── */
/* Only target the ICON SPAN elements inside the buttons — not the button/div wrappers,
   to avoid overriding Streamlit's native visibility:hidden on the collapse button */
[data-testid="stIconMaterial"],
[data-testid="stSidebarCollapseButton"] span,
[data-testid="stExpandSidebarButton"] span,
button[aria-label="Collapse sidebar"] span,
button[aria-label="Expand sidebar"] span,
.material-symbols-rounded,
.material-symbols-outlined,
.material-icons {
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
    font-size: 20px !important;
    font-style: normal !important;
    font-weight: 400 !important;
    line-height: 1 !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    display: inline-block !important;
    white-space: nowrap !important;
    word-wrap: normal !important;
    direction: ltr !important;
    -webkit-font-smoothing: antialiased !important;
    text-rendering: optimizeLegibility !important;
    -moz-osx-font-smoothing: grayscale !important;
    font-feature-settings: 'liga' !important;
}

/* ── Sidebar Layout & Anti-Clipping ────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0f23 0%, #1a1a3e 100%) !important;
    border-right: 1px solid rgba(99,102,241,0.2) !important;
    min-width: 270px !important;
}

/* ── Make stSidebarContent a flex column so we can reorder children ── */
[data-testid="stSidebarContent"] {
    display: flex !important;
    flex-direction: column !important;
}

/* stSidebarHeader (collapse button row) stays at very top — order 0 */
[data-testid="stSidebarHeader"] {
    order: 0 !important;
    flex-shrink: 0 !important;
}

/* stSidebarUserContent (our brand "Sentiment AI") goes SECOND — order 1 */
[data-testid="stSidebarUserContent"] {
    order: 1 !important;
    flex-shrink: 0 !important;
    padding: 0.25rem 0.75rem 0.5rem !important;
    overflow-x: hidden !important;
}

/* stSidebarNav (page links) goes THIRD — order 2 */
[data-testid="stSidebarNav"] {
    order: 2 !important;
    flex-shrink: 0 !important;
    overflow: visible !important;
    padding-top: 0 !important;
}

/* ── Sidebar Brand Header styling ─────────────────────────── */
.sidebar-brand-header {
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    padding: 0.4rem 0.25rem 0.75rem !important;
    border-bottom: 1px solid rgba(99,102,241,0.2) !important;
    margin-bottom: 0.25rem !important;
}

[data-testid="stSidebarNav"] ul {
    padding-left: 0 !important;
    margin: 0 !important;
}

[data-testid="stSidebarNav"] li {
    list-style: none !important;
    margin-bottom: 3px !important;
}

[data-testid="stSidebarNav"] a {
    color: #cbd5e1 !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
    padding: 0.45rem 0.75rem !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
    display: flex !important;
    align-items: center !important;
}

[data-testid="stSidebarNav"] a:hover {
    color: #ffffff !important;
    background: rgba(99,102,241,0.18) !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    color: #ffffff !important;
    background: rgba(99,102,241,0.28) !important;
    font-weight: 700 !important;
    border-left: 3px solid #818cf8 !important;
}

/* ── Collapse Sidebar Button: let Streamlit's native hover JS control this ── */
/* Only subtle color tweak — DO NOT override visibility or display */
[data-testid="stSidebarCollapseButton"] button:hover {
    background: rgba(99,102,241,0.15) !important;
    border-radius: 6px !important;
}

/* ── Expand Sidebar Button (when sidebar is CLOSED) ────────── */
[data-testid="stExpandSidebarButton"],
button[aria-label="Expand sidebar"] {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    position: fixed !important;
    top: 0.75rem !important;
    left: 0.75rem !important;
    z-index: 999999 !important;
    background: #1e1e3f !important;
    border: 1px solid rgba(99,102,241,0.5) !important;
    border-radius: 8px !important;
    padding: 0.4rem 0.65rem !important;
    color: #818cf8 !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.5) !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

[data-testid="stExpandSidebarButton"]:hover,
button[aria-label="Expand sidebar"]:hover {
    background: #2d2d5a !important;
    border-color: #818cf8 !important;
    transform: scale(1.05) !important;
}

[data-testid="stExpandSidebarButton"] span,
button[aria-label="Expand sidebar"] span {
    color: #818cf8 !important;
}

/* ── Hide Deploy Button & Native Watermarks ─────────────────── */
[data-testid="stAppDeployButton"],
.stAppDeployButton,
.stDeployButton,
#MainMenu,
footer {
    display: none !important;
    visibility: hidden !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

/* ── Metric Cards ──────────────────────────────────────────── */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1e1e3f 0%, #16213e 100%) !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
div[data-testid="metric-container"] label {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}

/* ── Action Buttons ────────────────────────────────────────── */
div.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
}
div.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.4) !important;
}

/* Quick Example buttons & compact buttons in columns */
div[data-testid="column"] div.stButton > button {
    padding: 0.35rem 0.35rem !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    white-space: nowrap !important;
    letter-spacing: -0.01em !important;
}

/* ── Inputs ────────────────────────────────────────────────── */
textarea, input[type="text"] {
    background: #1e1e3f !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}

/* ── Sentiment Badges ──────────────────────────────────────── */
.badge-positive { background:#052e16; color:#10b981; border:1px solid #10b981; }
.badge-negative { background:#450a0a; color:#ef4444; border:1px solid #ef4444; }
.badge-neutral  { background:#1e1b4b; color:#818cf8; border:1px solid #6366f1; }
.sentiment-badge {
    display: inline-block; padding: 0.35rem 1rem;
    border-radius: 9999px; font-weight: 700;
    font-size: 1.05rem; letter-spacing: 0.02em;
}

/* ── Cards & Dataframes ────────────────────────────────────── */
.card {
    background: linear-gradient(135deg, #1e1e3f 0%, #16213e 100%);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* ── Clickable Module Cards (Zero Underline) ──────────────── */
a.module-card-link,
.module-card-link,
.module-card-link *,
.module-card-link:hover,
.module-card-link:hover *,
.module-card-link:visited,
.module-card-link:visited *,
.module-card-link:active,
.module-card-link:focus,
.stMarkdown a.module-card-link,
.stMarkdown a.module-card-link * {
    text-decoration: none !important;
    text-decoration-line: none !important;
}

.module-card-link {
    display: block !important;
    color: inherit !important;
    margin-bottom: 1rem !important;
}

.module-card-link .card {
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    margin-bottom: 0 !important;
    height: 100% !important;
    text-decoration: none !important;
}

.module-card-link:hover .card {
    transform: translateY(-4px) !important;
    border-color: #818cf8 !important;
    background: linear-gradient(135deg, #25254f 0%, #1a254d 100%) !important;
    box-shadow: 0 8px 24px rgba(99,102,241,0.28) !important;
}

.module-card-link:hover .card div[style*="color:#f8fafc"] {
    color: #ffffff !important;
}

/* ── Tabs ──────────────────────────────────────────────────── */
button[data-baseweb="tab"] {
    background: transparent; color: #94a3b8 !important;
    border-radius: 8px 8px 0 0; font-weight: 500;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: rgba(99,102,241,0.15) !important;
    color: #818cf8 !important; border-bottom: 2px solid #6366f1;
}

/* ── Divider ───────────────────────────────────────────────── */
hr { border-color: rgba(99,102,241,0.2) !important; }
</style>
"""


def apply_custom_styles():
    """Inject global CSS and Lucide Icons scripts into Streamlit."""
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown(LUCIDE_CDN, unsafe_allow_html=True)
