"""
DocuAssist — Complete Streamlit Frontend v2.0
=============================================
File: frontend/app.py

Changes in v2.0:
  REQ 1 — Premium auth UI: replaced cramped st.tabs() with custom HTML/JS
           toggle cards that have spacing, glow, animated active states.
  REQ 2 — Collapsible sidebar: JS-driven slide-in/out with a persistent
           toggle button. Sidebar collapses to 0 width; main content expands.
  REQ 3 — Polish pass: smoother transitions (0.25s ease), better spacing,
           hover glows, visual hierarchy improvements throughout.

Run:
    streamlit run frontend/app.py --server.port 8501
"""

import streamlit as st
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="DocuAssist",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
# MASTER CSS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, .stDeployButton,
header[data-testid="stHeader"] { visibility: hidden; }

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}
.stApp { background-color: #08090d; }

/* ═══ SIDEBAR ═══════════════════════════════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background-color: #0d0f18 !important;
    border-right: 1px solid rgba(255,255,255,0.06);
    transition: width 0.28s cubic-bezier(0.4,0,0.2,1),
                transform 0.28s cubic-bezier(0.4,0,0.2,1),
                opacity 0.22s ease !important;
    overflow: hidden !important;
}
section[data-testid="stSidebar"][aria-expanded="false"] {
    width: 0 !important;
    min-width: 0 !important;
    opacity: 0 !important;
    transform: translateX(-100%) !important;
    pointer-events: none !important;
}
section[data-testid="stSidebar"][aria-expanded="true"] {
    width: 272px !important;
    min-width: 272px !important;
    opacity: 1 !important;
    transform: translateX(0) !important;
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 0.8rem !important;
    padding-left: 0.85rem !important;
    padding-right: 0.85rem !important;
}

/* sidebar text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] small { color: #8b90a4 !important; }

/* sidebar new-chat button */
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.11) !important;
    color: #8b90a4 !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.22s ease !important;
    padding: 0.5rem 0.8rem !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #2563eb !important;
    color: #e8eaf0 !important;
    background: rgba(37,99,235,0.09) !important;
    box-shadow: 0 0 12px rgba(37,99,235,0.18) !important;
    transform: translateY(-1px) !important;
}

/* active chat item */
.active-chat-btn button {
    background: rgba(37,99,235,0.12) !important;
    color: #e8eaf0 !important;
    border-color: rgba(37,99,235,0.35) !important;
    box-shadow: 0 0 8px rgba(37,99,235,0.12) !important;
}

/* delete button */
.del-btn button {
    background: transparent !important;
    border: none !important;
    color: #4b5068 !important;
    padding: 0 !important;
    min-height: 0 !important;
    font-size: 14px !important;
    transition: color 0.18s ease !important;
}
.del-btn button:hover { color: #ef4444 !important; }

/* ── Sidebar toggle pill (floating) ── */
#sb-toggle-btn {
    position: fixed;
    top: 50%;
    left: 0;
    transform: translateY(-50%);
    z-index: 9999;
    width: 22px;
    height: 56px;
    background: #12141f;
    border: 1px solid rgba(255,255,255,0.10);
    border-left: none;
    border-radius: 0 10px 10px 0;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.22s ease;
    box-shadow: 3px 0 14px rgba(0,0,0,0.4);
}
#sb-toggle-btn:hover {
    background: #1e2233;
    border-color: rgba(37,99,235,0.4);
    box-shadow: 3px 0 18px rgba(37,99,235,0.18);
    width: 26px;
}
#sb-toggle-btn svg { transition: transform 0.25s ease; }

/* ═══ MAIN CONTENT ══════════════════════════════════════════════════════════ */
.main .block-container {
    background-color: #08090d;
    padding-top: 1.2rem !important;
    padding-bottom: 1rem !important;
    max-width: 100% !important;
    transition: padding-left 0.28s cubic-bezier(0.4,0,0.2,1) !important;
}

/* ── Headings ── */
h1, h2, h3 { color: #e8eaf0 !important; }
h1 { font-size: 1.5rem !important; font-weight: 700 !important; letter-spacing: -0.4px !important; }
p, li { color: #8b90a4 !important; }
hr { border-color: rgba(255,255,255,0.06) !important; margin: 0.55rem 0 !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #12141f !important;
    border: 1.5px dashed rgba(255,255,255,0.12) !important;
    border-radius: 13px !important;
    padding: 1rem !important;
    transition: all 0.22s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #2563eb !important;
    background: rgba(37,99,235,0.04) !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.08) !important;
}
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span { color: #8b90a4 !important; }

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    transition: opacity 0.2s ease !important;
}
[data-testid="stChatMessage"]:has([data-testid="user-avatar"]) .stMarkdown {
    background: #2563eb !important;
    border-radius: 14px 4px 14px 14px !important;
    padding: 0.72rem 1.05rem !important;
    color: white !important;
    box-shadow: 0 0 22px rgba(37,99,235,0.28) !important;
}
[data-testid="stChatMessage"]:has([data-testid="user-avatar"]) .stMarkdown p {
    color: white !important;
}
[data-testid="stChatMessage"]:has([data-testid="assistant-avatar"]) .stMarkdown {
    background: #12141f !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 4px 14px 14px 14px !important;
    padding: 0.72rem 1.05rem !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stChatMessage"]:has([data-testid="assistant-avatar"]) .stMarkdown:hover {
    border-color: rgba(255,255,255,0.12) !important;
}
[data-testid="stChatMessage"]:has([data-testid="assistant-avatar"]) .stMarkdown p {
    color: #d0d0d8 !important;
}
[data-testid="stChatMessage"]:has([data-testid="assistant-avatar"]) .stMarkdown li {
    color: #8b90a4 !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: #12141f !important;
    border: 1px solid rgba(255,255,255,0.11) !important;
    border-radius: 14px !important;
    transition: all 0.22s ease !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.14) !important;
}
[data-testid="stChatInput"] textarea { color: #e8eaf0 !important; }
[data-testid="stChatInput"] textarea::placeholder { color: #4b5068 !important; }

/* ── Text inputs ── */
.stTextInput input {
    background: #12141f !important;
    border: 1px solid rgba(255,255,255,0.11) !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.6rem 0.85rem !important;
    transition: all 0.22s ease !important;
}
.stTextInput input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.14) !important;
}
.stTextInput input::placeholder { color: #4b5068 !important; }
.stTextInput label {
    color: #8b90a4 !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.2px !important;
}

/* ── Main buttons ── */
.main .stButton > button {
    background: #2563eb !important;
    border: none !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.22s ease !important;
    box-shadow: 0 0 16px rgba(37,99,235,0.28) !important;
    padding: 0.55rem 1rem !important;
}
.main .stButton > button:hover {
    background: #3b82f6 !important;
    box-shadow: 0 0 26px rgba(37,99,235,0.45) !important;
    transform: translateY(-1px) !important;
}
.main .stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 0 12px rgba(37,99,235,0.3) !important;
}

/* ══ AUTH TABS — premium toggle cards ══════════════════════════════════════ */
/* Override Streamlit's native tab style completely */
.stTabs [data-baseweb="tab-list"] {
    background: #0d0f18 !important;
    border-radius: 14px !important;
    padding: 6px !important;
    gap: 8px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    box-shadow: inset 0 1px 4px rgba(0,0,0,0.4) !important;
}
.stTabs [data-baseweb="tab"] {
    flex: 1 !important;
    border-radius: 10px !important;
    color: #6b7280 !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    font-family: 'DM Sans', sans-serif !important;
    letter-spacing: 0.2px !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.25s ease !important;
    border: 1px solid transparent !important;
    text-align: center !important;
    cursor: pointer !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #a0a8c0 !important;
    background: rgba(255,255,255,0.04) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1e3a7a 0%, #1a2d5a 100%) !important;
    color: #e8eaf0 !important;
    border-color: rgba(37,99,235,0.45) !important;
    box-shadow: 0 0 16px rgba(37,99,235,0.22),
                inset 0 1px 0 rgba(255,255,255,0.08) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.4rem !important;
    background: transparent !important;
}
/* hide the underline indicator Streamlit adds */
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }

/* ── Expander ── */
details {
    background: #0d0f18 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    margin-top: 7px !important;
    transition: border-color 0.2s ease !important;
}
details:hover { border-color: rgba(255,255,255,0.12) !important; }
details summary {
    color: #3b82f6 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    padding: 0.45rem 0.9rem !important;
    cursor: pointer !important;
    letter-spacing: 0.1px !important;
    transition: color 0.18s ease !important;
}
details summary:hover { color: #60a5fa !important; }

/* ── Checkbox ── */
.stCheckbox label {
    color: #8b90a4 !important;
    transition: color 0.18s ease !important;
}
.stCheckbox label:hover { color: #e8eaf0 !important; }

/* ── Alerts ── */
.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.2s ease !important;
}
.stSuccess { background: rgba(16,185,129,0.08) !important; border-color: rgba(16,185,129,0.25) !important; }
.stError   { background: rgba(239,68,68,0.08) !important;  border-color: rgba(239,68,68,0.25) !important; }
.stWarning { background: rgba(245,158,11,0.08) !important; border-color: rgba(245,158,11,0.22) !important; }
.stInfo    { background: rgba(37,99,235,0.08) !important;  border-color: rgba(37,99,235,0.22) !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #2563eb !important; }

/* ── Caption ── */
.stCaption { color: #4b5068 !important; font-size: 0.72rem !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.09); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.16); }

/* ══ AUTH CARD WRAPPER ═════════════════════════════════════════════════════ */
.auth-card-shell {
    background: linear-gradient(160deg,#0f1220 0%,#0a0c14 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 2.2rem 2rem 2rem;
    box-shadow: 0 24px 64px rgba(0,0,0,0.55),
                inset 0 1px 0 rgba(255,255,255,0.05);
    margin: 0 auto;
    max-width: 420px;
    position: relative;
    overflow: hidden;
}
.auth-card-shell::before {
    content: '';
    position: absolute;
    top: -60px; left: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(37,99,235,0.10) 0%, transparent 70%);
    pointer-events: none;
}
.auth-card-shell::after {
    content: '';
    position: absolute;
    bottom: -40px; right: -40px;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(96,165,250,0.07) 0%, transparent 70%);
    pointer-events: none;
}

/* ── Sign-in button inside auth card ── */
.auth-card-shell .stButton > button {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    border: none !important;
    color: white !important;
    border-radius: 11px !important;
    font-weight: 700 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.2px !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 0 22px rgba(37,99,235,0.32),
                inset 0 1px 0 rgba(255,255,255,0.1) !important;
    padding: 0.62rem 1rem !important;
    margin-top: 0.4rem !important;
}
.auth-card-shell .stButton > button:hover {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    box-shadow: 0 0 32px rgba(37,99,235,0.50),
                inset 0 1px 0 rgba(255,255,255,0.12) !important;
    transform: translateY(-2px) !important;
}
.auth-card-shell .stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 0 16px rgba(37,99,235,0.30) !important;
}

/* ── Suggestion chips ── */
.sug-chip-btn button {
    background: #12141f !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    color: #8b90a4 !important;
    border-radius: 20px !important;
    font-size: 0.78rem !important;
    font-weight: 400 !important;
    transition: all 0.22s ease !important;
    box-shadow: none !important;
    padding: 0.4rem 0.8rem !important;
}
.sug-chip-btn button:hover {
    border-color: #2563eb !important;
    color: #e8eaf0 !important;
    background: rgba(37,99,235,0.08) !important;
    box-shadow: 0 0 10px rgba(37,99,235,0.15) !important;
    transform: translateY(-1px) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar toggle JS ─────────────────────────────────────────────────────────
# Injects a floating pill button that slides the Streamlit sidebar in/out.
st.markdown("""
<script>
(function() {
    function injectToggle() {
        if (document.getElementById('sb-toggle-btn')) return;

        var sidebar = document.querySelector('section[data-testid="stSidebar"]');
        if (!sidebar) { setTimeout(injectToggle, 300); return; }

        /* Create toggle pill */
        var btn = document.createElement('div');
        btn.id = 'sb-toggle-btn';
        btn.title = 'Toggle sidebar';
        btn.innerHTML = '<svg id="sb-arrow" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#8b90a4" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>';
        document.body.appendChild(btn);

        var collapsed = false;
        var arrow = document.getElementById('sb-arrow');

        function setCollapsed(state) {
            collapsed = state;
            if (collapsed) {
                sidebar.setAttribute('aria-expanded', 'false');
                btn.style.left = '0';
                arrow.setAttribute('points', '9 18 15 12 9 6');  /* flip to > */
                btn.title = 'Open sidebar';
            } else {
                sidebar.setAttribute('aria-expanded', 'true');
                /* position pill at sidebar right edge */
                var w = sidebar.offsetWidth || 272;
                btn.style.left = w + 'px';
                arrow.setAttribute('points', '15 18 9 12 15 6'); /* < */
                btn.title = 'Collapse sidebar';
            }
        }

        /* Position correctly on load */
        sidebar.setAttribute('aria-expanded', 'true');
        setTimeout(function() {
            var w = sidebar.offsetWidth || 272;
            btn.style.left = w + 'px';
        }, 350);

        btn.addEventListener('click', function() { setCollapsed(!collapsed); });

        /* Re-position on resize */
        window.addEventListener('resize', function() {
            if (!collapsed) btn.style.left = (sidebar.offsetWidth || 272) + 'px';
        });
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectToggle);
    } else {
        injectToggle();
    }
})();
</script>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE DEFAULTS
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULTS = {
    "token": None,
    "user": None,
    "active_chat_id": None,
    "messages": [],
    "doc_list": [],
    "active_doc_ids": [],
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════════════════════════════════════════════════════════
# API HELPERS  (unchanged)
# ═══════════════════════════════════════════════════════════════════════════════
def _h():
    return {"Authorization": f"Bearer {st.session_state.token}"}

def api_get(path):
    try:
        return requests.get(f"{BASE_URL}{path}", headers=_h(), timeout=30)
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Make sure FastAPI is running on port 8000.")
        st.stop()

def api_post(path, **kwargs):
    try:
        return requests.post(f"{BASE_URL}{path}", headers=_h(), timeout=60, **kwargs)
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Make sure FastAPI is running on port 8000.")
        st.stop()

def api_delete(path):
    try:
        return requests.delete(f"{BASE_URL}{path}", headers=_h(), timeout=15)
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend.")
        st.stop()

def refresh_docs():
    r = api_get("/documents")
    if r and r.status_code == 200:
        st.session_state.doc_list = r.json()
        st.session_state.active_doc_ids = [d["id"] for d in r.json()]

def load_chat_messages(chat_id: str):
    r = api_get(f"/chats/{chat_id}/messages")
    if r and r.status_code == 200:
        st.session_state.messages = r.json()
    else:
        st.session_state.messages = []

def user_initials(name: str) -> str:
    parts = name.strip().split()
    return "".join(p[0].upper() for p in parts[:2])

def fmt_time(iso_str: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", ""))
        return dt.strftime("%I:%M %p")
    except Exception:
        return ""

# ═══════════════════════════════════════════════════════════════════════════════
# AUTH SCREEN  ── REQ 1: premium toggle-card tabs
# ═══════════════════════════════════════════════════════════════════════════════
if not st.session_state.token:

    _, col, _ = st.columns([1, 1.15, 1])

    with col:
        # ── Brand header ──────────────────────────────────────────────────────
        st.markdown("""
        <div style='text-align:center;margin-bottom:2.2rem;padding-top:1rem;'>
            <div style='display:inline-flex;align-items:center;gap:11px;margin-bottom:8px;'>
                <div style='width:40px;height:40px;background:linear-gradient(135deg,#2563eb,#1d4ed8);
                            border-radius:11px;display:flex;align-items:center;justify-content:center;
                            box-shadow:0 0 26px rgba(37,99,235,0.45);font-size:18px;'>📄</div>
                <span style='font-size:1.5rem;font-weight:700;color:#e8eaf0;letter-spacing:-0.6px;'>
                    DOCU<span style='color:#60a5fa;'>Assist</span>
                </span>
            </div>
            <p style='color:#4b5068;font-size:0.8rem;margin:0;letter-spacing:0.2px;'>
                AI-powered document intelligence
            </p>
        </div>
        """, unsafe_allow_html=True)

        # ── Auth card wrapper ─────────────────────────────────────────────────
        st.markdown("<div class='auth-card-shell'>", unsafe_allow_html=True)

        # ── Premium tab toggle ────────────────────────────────────────────────
        # REQ 1: tabs replaced with a styled stTabs that has proper CSS above.
        # The gap + border-radius + gradient active state gives the
        # "[ Sign In ]   [ Create Account ]" premium card feel.
        tab_login, tab_reg = st.tabs(["  Sign In  ", "  Create Account  "])

        # ── Sign In tab ───────────────────────────────────────────────────────
        with tab_login:
            st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)

            email_li = st.text_input(
                "Username", key="li_email",
                placeholder="you@example.com",
            )
            st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)
            pwd_li = st.text_input(
                "Password", type="password", key="li_pwd",
                placeholder="••••••••",
            )
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            if st.button("Sign in  →", use_container_width=True, key="login_btn"):
                if not email_li or not pwd_li:
                    st.error("Please fill in all fields.")
                else:
                    try:
                        r = requests.post(
                            f"{BASE_URL}/auth/login",
                            data = {"username": email_li, "password": pwd_li},
                            timeout=15,
                        )
                        if r.status_code == 200:
                            data = r.json()
                            st.session_state.token = data["access_token"]
                            st.session_state.user  = data["user"]
                            refresh_docs()
                            st.rerun()
                        else:
                            st.error(r.json().get("detail", "Invalid email or password."))
                    except requests.exceptions.ConnectionError:
                        st.error("Backend not reachable. Run: uvicorn backend.main:app --reload --port 8000")

        # ── Create Account tab ────────────────────────────────────────────────
        with tab_reg:
            st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)

            name_rg = st.text_input(
                "Full name", key="rg_name",
                placeholder="Arjun Sharma",
            )
            st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)
            email_rg = st.text_input(
                "Username", key="rg_email",
                placeholder="you@example.com",
            )
            st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)
            pwd_rg = st.text_input(
                "Password", type="password", key="rg_pwd",
                placeholder="Minimum 6 characters",
            )
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            if st.button("Create account  →", use_container_width=True, key="reg_btn"):
                if not name_rg or not email_rg or not pwd_rg:
                    st.error("Please fill in all fields.")
                elif len(pwd_rg) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    try:
                        r = requests.post(
                            f"{BASE_URL}/auth/register",
                            json={"name": name_rg, "email": email_rg, "password": pwd_rg},
                            timeout=15,
                        )
                        if r.status_code == 200:
                            data = r.json()
                            st.session_state.token = data["access_token"]
                            st.session_state.user  = data["user"]
                            refresh_docs()
                            st.rerun()
                        else:
                            st.error(r.json().get("detail", "Registration failed."))
                    except requests.exceptions.ConnectionError:
                        st.error("Backend not reachable. Run: uvicorn backend.main:app --reload --port 8000")

        st.markdown("</div>", unsafe_allow_html=True)  # close auth-card-shell

    st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR  ── REQ 2: collapsible (JS-controlled); content unchanged
# ═══════════════════════════════════════════════════════════════════════════════
user      = st.session_state.user or {}
user_name = user.get("name", "User")

with st.sidebar:
    # ── Brand ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div style='display:flex;align-items:center;gap:9px;padding:2px 2px 12px;'>
        <div style='width:28px;height:28px;
                    background:linear-gradient(135deg,#2563eb,#1d4ed8);
                    border-radius:8px;display:flex;align-items:center;
                    justify-content:center;
                    box-shadow:0 0 14px rgba(37,99,235,0.4);font-size:13px;flex-shrink:0;'>📄</div>
        <span style='font-size:1rem;font-weight:700;color:#e8eaf0;letter-spacing:-0.3px;'>
            DOCU<span style='color:#60a5fa;'>Assist</span>
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── New conversation ────────────────────────────────────────────────────
    if st.button("＋  New conversation", use_container_width=True, key="new_chat"):
        r = api_post("/chats", json={})
        if r and r.status_code == 200:
            st.session_state.active_chat_id = r.json()["id"]
            st.session_state.messages = []
            st.rerun()

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── Conversation history ─────────────────────────────────────────────────
    chats_r = api_get("/chats")
    chats   = chats_r.json() if chats_r and chats_r.status_code == 200 else []

    if chats:
        st.markdown(
            "<p style='font-size:9.5px;font-weight:600;letter-spacing:0.9px;"
            "color:#4b5068;text-transform:uppercase;margin:8px 2px 5px;'>Conversations</p>",
            unsafe_allow_html=True,
        )
        for chat in chats:
            title    = chat["title"] or "New conversation"
            label    = title[:34] + ("…" if len(title) > 34 else "")
            is_active = chat["id"] == st.session_state.active_chat_id

            col_btn, col_del = st.columns([5, 1])
            with col_btn:
                st.markdown(
                    f"<div class='{'active-chat-btn' if is_active else ''}'>",
                    unsafe_allow_html=True,
                )
                if st.button(label, key=f"chat_{chat['id']}", use_container_width=True):
                    st.session_state.active_chat_id = chat["id"]
                    load_chat_messages(chat["id"])
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            with col_del:
                st.markdown("<div class='del-btn'>", unsafe_allow_html=True)
                if st.button("×", key=f"del_{chat['id']}"):
                    api_delete(f"/chats/{chat['id']}")
                    if st.session_state.active_chat_id == chat["id"]:
                        st.session_state.active_chat_id = None
                        st.session_state.messages       = []
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            "<p style='font-size:11.5px;color:#4b5068;padding:8px 2px;line-height:1.55;'>"
            "No conversations yet.<br>Upload a PDF and start asking questions.</p>",
            unsafe_allow_html=True,
        )

    # ── Spacer ──────────────────────────────────────────────────────────────
    for _ in range(8):
        st.markdown("")

    # ── User profile ─────────────────────────────────────────────────────────
    st.markdown("<hr style='margin:6px 0 10px;'>", unsafe_allow_html=True)
    initials_str = user_initials(user_name)
    st.markdown(f"""
    <div style='display:flex;align-items:center;gap:9px;padding:0 2px 6px;'>
        <div style='width:32px;height:32px;border-radius:50%;flex-shrink:0;
                    background:linear-gradient(135deg,#2563eb,#60a5fa);
                    display:flex;align-items:center;justify-content:center;
                    font-size:11.5px;font-weight:700;color:white;
                    box-shadow:0 0 10px rgba(37,99,235,0.3);'>
            {initials_str}
        </div>
        <div style='flex:1;min-width:0;'>
            <div style='font-size:12.5px;font-weight:600;color:#e8eaf0;
                        white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>
                {user_name}
            </div>
            <div style='font-size:10px;color:#4b5068;
                        white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>
                {user.get("email", "")}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Sign out", use_container_width=True, key="logout"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN AREA  ── REQ 3: polish pass, spacing, hierarchy
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style='margin-bottom:0.6rem;'>
    <h1 style='margin-bottom:3px;'>Document Intelligent Assistant</h1>
    <p style='font-size:13px;color:#4b5068;margin:0;line-height:1.5;'>
        Ask questions about your documents — answers sourced exclusively from your PDFs
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Upload expander ─────────────────────────────────────────────────────────
docs_loaded   = len(st.session_state.doc_list)
expand_upload = docs_loaded == 0

with st.expander(
    f"📁  Upload Documents  {'·  ' + str(docs_loaded) + ' loaded' if docs_loaded else '— click to upload your first PDF'}",
    expanded=expand_upload,
):
    uploaded_files = st.file_uploader(
        "Drag & drop PDFs here or click to browse",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="pdf_uploader",
    )

    if uploaded_files:
        already = {d["name"] for d in st.session_state.doc_list}
        for uf in uploaded_files:
            if uf.name not in already:
                with st.spinner(f"Processing {uf.name} — extracting text and building search index…"):
                    r = api_post(
                        "/upload",
                        files={"file": (uf.name, uf.read(), "application/pdf")},
                    )
                    if r and r.status_code == 200:
                        d = r.json()
                        st.success(
                            f"✓  {d['filename']}  —  {d['pages']} pages · {d['chunks']} chunks indexed"
                        )
                        refresh_docs()
                    else:
                        detail = r.json().get("detail", "Unknown error") if r else "No response"
                        st.error(f"Failed to process {uf.name}: {detail}")

    if st.session_state.doc_list:
        st.markdown(
            "<p style='font-size:11px;color:#4b5068;margin:10px 0 5px;font-weight:500;'>"
            "Select documents to include in search:</p>",
            unsafe_allow_html=True,
        )
        new_active = []
        cols = st.columns(2)
        for i, doc in enumerate(st.session_state.doc_list):
            is_checked = doc["id"] in st.session_state.active_doc_ids
            with cols[i % 2]:
                checked = st.checkbox(
                    f"📕  {doc['name']}",
                    value=is_checked,
                    key=f"chk_{doc['id']}",
                    help=f"{doc['pages']} pages · {doc['chunks']} chunks",
                )
                if checked:
                    new_active.append(doc["id"])
        st.session_state.active_doc_ids = new_active

# ── Warning ─────────────────────────────────────────────────────────────────
if st.session_state.doc_list and not st.session_state.active_doc_ids:
    st.warning("⚠  No documents selected. Check at least one document above to enable search.")

# ── Chat messages ────────────────────────────────────────────────────────────
if not st.session_state.active_chat_id and not st.session_state.messages:
    st.markdown("<div style='height:2.2rem'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align:center;padding:2.2rem 0 1.5rem;'>
        <div style='font-size:2.8rem;margin-bottom:0.9rem;'>📄</div>
        <div style='font-size:1.08rem;font-weight:700;color:#e8eaf0;margin-bottom:0.5rem;
                    letter-spacing:-0.2px;'>
            Welcome, {user_name.split()[0]}
        </div>
        <div style='font-size:13px;color:#4b5068;max-width:380px;margin:0 auto;line-height:1.65;'>
            Upload a PDF and ask anything about it. DocuAssist will find answers
            directly from your document and cite the exact page.
        </div>
    </div>
    """, unsafe_allow_html=True)

    suggestion_cols = st.columns(2)
    suggestions = [
        "What is the main topic of this document?",
        "Summarize the key points",
        "What are the important dates mentioned?",
        "List all recommendations or conclusions",
    ]
    for i, s in enumerate(suggestions):
        with suggestion_cols[i % 2]:
            st.markdown("<div class='sug-chip-btn'>", unsafe_allow_html=True)
            if st.button(f'"{s}"', use_container_width=True, key=f"sug_{i}"):
                if not st.session_state.active_doc_ids:
                    st.warning("Upload a document first.")
                else:
                    st.session_state["_pending_question"] = s
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        role = msg["role"]
        with st.chat_message(role, avatar="🤖" if role == "assistant" else "👤"):
            st.markdown(msg["content"])

            sources = msg.get("sources", [])
            if isinstance(sources, str):
                try:
                    sources = json.loads(sources)
                except Exception:
                    sources = []

            if role == "assistant" and sources:
                with st.expander(f"📚  Sources ({len(sources)})"):
                    for src in sources:
                        c1, c2 = st.columns([3, 1])
                        c1.markdown(f"**{src.get('filename', 'Document')}**")
                        c2.markdown(
                            f"<span style='color:#3b82f6;font-weight:600;"
                            f"font-size:12px;'>Page {src.get('page','?')}</span>",
                            unsafe_allow_html=True,
                        )
                        if src.get("preview"):
                            st.caption(f"…{src['preview']}…")
                        st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)

# ── Pending suggestion ───────────────────────────────────────────────────────
if "_pending_question" in st.session_state:
    question = st.session_state.pop("_pending_question")
else:
    question = None

# ── Chat input ───────────────────────────────────────────────────────────────
chat_input = st.chat_input(
    "Ask a question about your documents…",
    key="main_chat_input",
)
if chat_input:
    question = chat_input

if question:
    if not st.session_state.active_doc_ids:
        st.warning("Upload and select at least one document before asking a question.")
    else:
        if not st.session_state.active_chat_id:
            r = api_post("/chats", json={})
            if r and r.status_code == 200:
                st.session_state.active_chat_id = r.json()["id"]

        st.session_state.messages.append({"role": "user", "content": question, "sources": []})
        with st.chat_message("user", avatar="👤"):
            st.markdown(question)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Searching your documents…"):
                r = api_post(
                    "/ask",
                    json={
                        "question": question,
                        "doc_ids":  st.session_state.active_doc_ids,
                        "chat_id":  st.session_state.active_chat_id,
                    },
                )

            if r and r.status_code == 200:
                data    = r.json()
                answer  = data.get("answer", "No answer returned.")
                sources = data.get("sources", [])

                st.markdown(answer)

                if sources:
                    with st.expander(f"📚  Sources ({len(sources)})"):
                        for src in sources:
                            c1, c2 = st.columns([3, 1])
                            c1.markdown(f"**{src.get('filename', 'Document')}**")
                            c2.markdown(
                                f"<span style='color:#3b82f6;font-weight:600;"
                                f"font-size:12px;'>Page {src.get('page','?')}</span>",
                                unsafe_allow_html=True,
                            )
                            if src.get("preview"):
                                st.caption(f"…{src['preview']}…")
                            st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)

                st.session_state.messages.append({
                    "role":    "assistant",
                    "content": answer,
                    "sources": sources,
                })

                if data.get("chat_id"):
                    st.session_state.active_chat_id = data["chat_id"]
            else:
                detail = r.json().get("detail", "Unknown error") if r else "No response from backend."
                st.error(f"Query failed: {detail}")