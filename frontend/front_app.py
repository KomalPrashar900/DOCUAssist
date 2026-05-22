
import streamlit as st
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api")

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DocuAssist",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state ──────────────────────────────────────────────────────────────
for k, v in {
    "token": None, "user": None,
    "active_chat_id": None, "messages": [],
    "doc_list": [], "active_doc_ids": [],
    "auth_tab": "login",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── API helpers ────────────────────────────────────────────────────────────────
def hdr():
    return {"Authorization": f"Bearer {st.session_state.token}"}

def api_get(path):
    try:
        return requests.get(f"{BASE_URL}{path}", headers=hdr(), timeout=30)
    except Exception:
        return None

def api_post(path, **kw):
    try:
        return requests.post(f"{BASE_URL}{path}", headers=hdr(), timeout=60, **kw)
    except Exception:
        return None

def api_del(path):
    try:
        return requests.delete(f"{BASE_URL}{path}", headers=hdr(), timeout=15)
    except Exception:
        return None

def refresh_docs():
    r = api_get("/documents")
    if r and r.status_code == 200:
        st.session_state.doc_list = r.json()
        st.session_state.active_doc_ids = [d["id"] for d in r.json()]

def load_msgs(chat_id):
    r = api_get(f"/chats/{chat_id}/messages")
    st.session_state.messages = r.json() if r and r.status_code == 200 else []

def initials(name):
    return "".join(p[0].upper() for p in str(name).strip().split()[:2]) or "U"

def now_ts():
    return datetime.now().strftime("%I:%M %p")

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* ── hide everything Streamlit ── */
#MainMenu, footer, .stDeployButton,
header[data-testid="stHeader"],
[data-testid="collapsedControl"],
section[data-testid="stSidebar"],
.stAppViewBlockContainer > div:first-child > div:first-child > div > div[data-testid="column"] > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] { border:none !important; }

#MainMenu { visibility:hidden !important; }
footer    { visibility:hidden !important; }
.stDeployButton { display:none !important; }
header[data-testid="stHeader"] { display:none !important; }
[data-testid="collapsedControl"] { display:none !important; }
section[data-testid="stSidebar"] { display:none !important; }

html,body,[class*="css"] { font-family:'DM Sans',sans-serif !important; }
.stApp { background:#0c0d12 !important; }

/* ── block-container: full width, no padding ── */
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── column border reset ── */
[data-testid="column"] { padding:0 !important; }

/* ═══════════════════════════════════════════
   SIDEBAR COLUMN
═══════════════════════════════════════════ */
.sb-wrap {
    width:100%;
    height:100vh;
    background:#111318;
    border-right:1px solid rgba(255,255,255,0.07);
    display:flex;
    flex-direction:column;
    overflow:hidden;
}

/* brand */
.sb-brand {
    display:flex; align-items:center; gap:12px;
    padding:18px 16px 14px;
    border-bottom:1px solid rgba(255,255,255,0.06);
    flex-shrink:0;
}
.sb-brand-icon {
    width:38px; height:38px;
    background:#5c6bc0; border-radius:9px;
    display:flex; align-items:center; justify-content:center;
    font-size:19px; flex-shrink:0;
    box-shadow:0 0 18px rgba(92,107,192,0.35);
}
.sb-brand-name { font-size:1rem; font-weight:700; color:#e8eaf0; letter-spacing:-.3px; }
.sb-brand-sub  { font-size:11px; color:#4b5068; margin-top:1px; }

/* section labels */
.sb-label {
    font-size:9.5px; font-weight:700;
    letter-spacing:1px; color:#4b5068;
    text-transform:uppercase;
    padding:14px 16px 5px;
}

/* upload zone */
.sb-drop {
    margin:0 12px 8px;
    border:1.5px dashed rgba(255,255,255,0.13);
    border-radius:11px; padding:14px 10px;
    text-align:center; cursor:pointer;
    transition:all .2s;
    background:#161820;
}
.sb-drop:hover { border-color:#5c6bc0; background:rgba(92,107,192,0.05); }
.sb-drop-icon { font-size:18px; margin-bottom:5px; opacity:.55; }
.sb-drop-txt  { font-size:12px; color:#6b7280; line-height:1.5; }
.sb-drop-txt span { color:#7986cb; font-weight:500; }

/* doc item */
.sb-doc {
    display:flex; align-items:center; gap:10px;
    padding:9px 14px; margin:1px 8px;
    border-radius:9px; cursor:pointer;
    transition:background .15s;
    border:1px solid transparent;
}
.sb-doc:hover { background:#1a1d27; }
.sb-doc.on    { background:rgba(92,107,192,0.12); border-color:rgba(92,107,192,0.25); }
.sb-doc-icon  {
    width:30px; height:30px;
    background:rgba(239,68,68,0.13); border-radius:7px;
    display:flex; align-items:center; justify-content:center;
    font-size:13px; flex-shrink:0;
}
.sb-doc-name  { font-size:12.5px; font-weight:500; color:#d0d0d8;
                white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.sb-doc-meta  { font-size:10.5px; color:#4b5068; margin-top:1px; }
.sb-doc-chk   {
    width:17px; height:17px; border-radius:50%;
    background:rgba(16,185,129,0.12);
    border:1px solid rgba(16,185,129,0.3);
    display:flex; align-items:center; justify-content:center;
    font-size:8px; color:#10b981; flex-shrink:0;
}

/* history scroll */
.sb-hist {
    flex:1; overflow-y:auto;
    padding:0 8px;
    min-height:0;
}
.sb-hist::-webkit-scrollbar { width:2px; }
.sb-hist::-webkit-scrollbar-thumb { background:rgba(255,255,255,0.08); border-radius:2px; }

.sb-hist-item {
    display:flex; align-items:center; gap:8px;
    padding:7px 8px; border-radius:8px;
    cursor:pointer; transition:background .15s;
    margin-bottom:2px;
}
.sb-hist-item:hover { background:#1a1d27; }
.sb-hist-item.on    { background:rgba(92,107,192,0.12); }
.sb-hist-dot {
    width:5px; height:5px; border-radius:50%;
    background:#5c6bc0; opacity:.35; flex-shrink:0;
}
.sb-hist-item.on .sb-hist-dot { opacity:1; }
.sb-hist-txt {
    font-size:12.5px; color:#6b7280;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis; flex:1;
}
.sb-hist-item.on .sb-hist-txt { color:#d0d0d8; }

/* user row */
.sb-user {
    padding:12px 14px;
    border-top:1px solid rgba(255,255,255,0.06);
    display:flex; align-items:center; gap:10px;
    flex-shrink:0;
}
.sb-av {
    width:32px; height:32px; border-radius:50%;
    background:linear-gradient(135deg,#5c6bc0,#7986cb);
    display:flex; align-items:center; justify-content:center;
    font-size:12px; font-weight:700; color:#fff; flex-shrink:0;
    box-shadow:0 0 10px rgba(92,107,192,0.28);
}
.sb-uname { font-size:13px; font-weight:600; color:#e8eaf0;
            white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.sb-uplan { font-size:10.5px; color:#f59e0b; margin-top:1px; }

/* ═══════════════════════════════════════════
   MAIN AREA
═══════════════════════════════════════════ */
.main-wrap {
    height:100vh;
    display:flex; flex-direction:column;
    background:#0c0d12;
    overflow:hidden;
}

/* topbar */
.topbar {
    display:flex; align-items:center; justify-content:space-between;
    padding:16px 24px;
    border-bottom:1px solid rgba(255,255,255,0.06);
    flex-shrink:0;
}
.topbar-title { font-size:1.3rem; font-weight:700; color:#e8eaf0; letter-spacing:-.4px; }
.topbar-sub   { font-size:12px; color:#4b5068; margin-top:3px; line-height:1.4; }
.new-chat-btn {
    padding:10px 18px;
    background:#1a1d27;
    border:1px solid rgba(255,255,255,0.13);
    border-radius:10px; color:#e8eaf0;
    font-size:13px; font-weight:600;
    font-family:'DM Sans',sans-serif;
    cursor:pointer; transition:all .2s;
    display:flex; align-items:center; gap:7px;
    white-space:nowrap;
}
.new-chat-btn:hover {
    background:#21253a;
    border-color:rgba(92,107,192,0.4);
    box-shadow:0 0 14px rgba(92,107,192,0.15);
}

/* messages */
.msgs-wrap {
    flex:1; overflow-y:auto;
    padding:24px; min-height:0;
    display:flex; flex-direction:column; gap:18px;
}
.msgs-wrap::-webkit-scrollbar { width:3px; }
.msgs-wrap::-webkit-scrollbar-thumb { background:rgba(255,255,255,0.09); border-radius:2px; }

/* user bubble */
.msg-row-user {
    display:flex; justify-content:flex-end;
    align-items:flex-start; gap:10px;
}
.bubble-user {
    background:#7c6af7; color:#fff;
    padding:13px 17px;
    border-radius:18px 4px 18px 18px;
    font-size:14px; line-height:1.65;
    max-width:72%;
    box-shadow:0 0 22px rgba(124,106,247,0.25);
}
.av-sm {
    width:32px; height:32px; border-radius:50%;
    background:linear-gradient(135deg,#5c6bc0,#7986cb);
    display:flex; align-items:center; justify-content:center;
    font-size:11px; font-weight:700; color:#fff; flex-shrink:0;
    margin-top:2px;
}
.msg-ts {
    font-size:10px; color:#3a3d50;
    text-align:right; margin-top:4px;
}

/* bot bubble */
.msg-row-bot {
    display:flex; align-items:flex-start; gap:12px;
}
.bot-av {
    width:34px; height:34px; border-radius:50%;
    background:#5c6bc0;
    display:flex; align-items:center; justify-content:center;
    font-size:16px; flex-shrink:0; margin-top:2px;
    box-shadow:0 0 14px rgba(92,107,192,0.3);
}
.bubble-bot {
    background:#161820;
    border:1px solid rgba(255,255,255,0.08);
    color:#d0d0d8; padding:13px 17px;
    border-radius:4px 18px 18px 18px;
    font-size:14px; line-height:1.7; max-width:80%;
    transition:border-color .2s;
}
.bubble-bot:hover { border-color:rgba(255,255,255,0.14); }

/* source cards */
.src-hdr {
    font-size:11.5px; color:#7986cb; font-weight:600;
    margin-top:10px; margin-bottom:5px;
    display:flex; align-items:center; gap:5px;
}
.src-card {
    display:flex; align-items:center; gap:9px;
    padding:7px 10px;
    background:#0c0d12;
    border:1px solid rgba(255,255,255,0.07);
    border-radius:9px; margin-bottom:4px;
    transition:all .15s;
}
.src-card:hover { border-color:rgba(92,107,192,0.35); background:rgba(92,107,192,0.05); }
.src-ico {
    width:22px; height:22px;
    background:rgba(239,68,68,0.12); border-radius:5px;
    display:flex; align-items:center; justify-content:center;
    font-size:10px; flex-shrink:0;
}
.src-fname { font-size:11px; font-weight:600; color:#d0d0d8; }
.src-pg    { font-size:10px; color:#4b5068; margin-top:1px; }
.src-prev  { font-size:10.5px; color:#4b5068;
             white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:210px; }

/* typing dots */
.typing {
    display:flex; gap:4px; align-items:center; padding:3px 0;
}
.td {
    width:7px; height:7px; border-radius:50%;
    background:#5c6bc0;
    animation:td 1.2s ease-in-out infinite;
}
.td:nth-child(2) { animation-delay:.2s; }
.td:nth-child(3) { animation-delay:.4s; }
@keyframes td {
    0%,80%,100%{ opacity:.25; transform:scale(.75); }
    40%{ opacity:1; transform:scale(1); }
}

/* empty state */
.empty-state {
    flex:1; display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    gap:12px; text-align:center; padding:2rem;
    color:#4b5068;
}
.empty-icon { font-size:3rem; margin-bottom:4px;
              filter:drop-shadow(0 0 16px rgba(92,107,192,0.3)); }
.empty-title { font-size:1.08rem; font-weight:700; color:#e8eaf0; }
.empty-sub   { font-size:13px; color:#4b5068;
               max-width:360px; line-height:1.65; }

/* input bar */
.input-bar {
    padding:14px 24px 18px;
    border-top:1px solid rgba(255,255,255,0.06);
    flex-shrink:0;
}

/* warn */
.warn-bar {
    display:flex; align-items:center; gap:8px;
    padding:9px 14px;
    background:rgba(245,158,11,0.07);
    border:1px solid rgba(245,158,11,0.18);
    border-radius:9px; margin-bottom:10px;
    font-size:12px; color:#f59e0b;
}

/* ── streamlit widget overrides ── */
.stChatInput > div {
    background:#161820 !important;
    border:1px solid rgba(255,255,255,0.12) !important;
    border-radius:14px !important;
}
.stChatInput > div:focus-within {
    border-color:#5c6bc0 !important;
    box-shadow:0 0 0 3px rgba(92,107,192,0.14) !important;
}
.stChatInput textarea { color:#e8eaf0 !important; font-family:'DM Sans',sans-serif !important; }
.stChatInput textarea::placeholder { color:#3a3d50 !important; }

.stButton > button {
    background:#5c6bc0 !important;
    border:none !important; border-radius:10px !important;
    color:#fff !important; font-family:'DM Sans',sans-serif !important;
    font-weight:600 !important; font-size:13px !important;
    transition:all .2s !important;
    box-shadow:0 0 14px rgba(92,107,192,0.25) !important;
}
.stButton > button:hover {
    background:#7986cb !important;
    box-shadow:0 0 22px rgba(92,107,192,0.4) !important;
    transform:translateY(-1px) !important;
}

/* sidebar column buttons */
section .stButton > button,
[data-testid="column"] .stButton > button {
    background:#1a1d27 !important;
    border:1px solid rgba(255,255,255,0.09) !important;
    color:#8b90a4 !important;
    box-shadow:none !important;
    border-radius:8px !important;
    font-size:12.5px !important;
    padding:5px 8px !important;
}
[data-testid="column"] .stButton > button:hover {
    border-color:#5c6bc0 !important;
    color:#e8eaf0 !important;
    background:rgba(92,107,192,0.10) !important;
    transform:none !important;
}

.stFileUploader {
    background:#161820 !important;
    border:1.5px dashed rgba(255,255,255,0.12) !important;
    border-radius:11px !important;
    padding:0.6rem !important;
}
.stFileUploader:hover { border-color:#5c6bc0 !important; }
.stFileUploader label { color:#8b90a4 !important; }
.stFileUploader [data-testid="stFileUploaderDropzone"] { background:transparent !important; }

.stTextInput input {
    background:#161820 !important;
    border:1px solid rgba(255,255,255,0.11) !important;
    border-radius:10px !important; color:#e8eaf0 !important;
    font-family:'DM Sans',sans-serif !important;
}
.stTextInput input:focus {
    border-color:#5c6bc0 !important;
    box-shadow:0 0 0 3px rgba(92,107,192,0.14) !important;
}
.stTextInput label { color:#6b7280 !important; font-size:12px !important; }

.stTabs [data-baseweb="tab-list"] {
    background:#0d0f18 !important; border-radius:12px !important;
    padding:5px !important; gap:7px !important;
    border:1px solid rgba(255,255,255,0.07) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius:9px !important; color:#4b5068 !important;
    font-weight:600 !important; font-size:13px !important;
    font-family:'DM Sans',sans-serif !important;
    padding:8px 18px !important; border:1px solid transparent !important;
    transition:all .22s !important;
}
.stTabs [data-baseweb="tab"]:hover { color:#8b90a4 !important; }
.stTabs [aria-selected="true"] {
    background:linear-gradient(135deg,#1e2a5a,#19234a) !important;
    color:#e8eaf0 !important;
    border-color:rgba(92,107,192,0.4) !important;
    box-shadow:0 0 14px rgba(92,107,192,0.18) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display:none !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top:1.2rem !important; }

.stSuccess { background:rgba(16,185,129,0.08) !important; border-color:rgba(16,185,129,0.25) !important; border-radius:9px !important; }
.stError   { background:rgba(239,68,68,0.08) !important;  border-color:rgba(239,68,68,0.22) !important;  border-radius:9px !important; }
.stWarning { background:rgba(245,158,11,0.08) !important; border-color:rgba(245,158,11,0.2) !important;  border-radius:9px !important; }
.stSpinner > div { border-top-color:#5c6bc0 !important; }
.stCheckbox label { color:#6b7280 !important; }

::-webkit-scrollbar { width:3px; }
::-webkit-scrollbar-thumb { background:rgba(255,255,255,0.09); border-radius:2px; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# AUTH SCREEN
# ═══════════════════════════════════════════════════════════════════════════════
if not st.session_state.token:
    _, mid, _ = st.columns([1, 1.1, 1])
    with mid:
        # Logo
        st.markdown("""
        <div style="text-align:center;padding:2.5rem 0 1.8rem;">
            <div style="display:inline-flex;align-items:center;gap:13px;margin-bottom:10px;">
                <div style="width:44px;height:44px;background:#5c6bc0;border-radius:12px;
                            display:flex;align-items:center;justify-content:center;font-size:21px;
                            box-shadow:0 0 28px rgba(92,107,192,0.4);">📄</div>
                <span style="font-size:1.6rem;font-weight:700;color:#e8eaf0;letter-spacing:-.5px;">
                    DocuAssist
                </span>
            </div>
            <div style="font-size:12px;color:#4b5068;letter-spacing:.2px;">
                AI Document Intelligence
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Card
        st.markdown("""
        <div style="background:linear-gradient(160deg,#0f1220,#0a0c14);
                    border:1px solid rgba(255,255,255,0.09);border-radius:20px;
                    padding:2.2rem 2rem 1.8rem;
                    box-shadow:0 24px 64px rgba(0,0,0,0.6),inset 0 1px 0 rgba(255,255,255,0.05);">
        """, unsafe_allow_html=True)

        tab_in, tab_up = st.tabs(["  Sign In  ", "  Create Account  "])

        with tab_in:
            email_li = st.text_input("Username", key="li_e", placeholder="you@example.com")
            pwd_li   = st.text_input("Password",      key="li_p", placeholder="••••••••", type="password")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            if st.button("Sign in →", key="btn_li", use_container_width=True):
                if not email_li or not pwd_li:
                    st.error("Please fill in all fields.")
                else:
                    try:
                        r = requests.post(
                            f"{BASE_URL}/auth/login",
                            data={
                                    "username": email_li,   # FIX HERE
                                    "password": pwd_li
                            },
                            timeout=15
                        )
                        
                        if r.status_code == 200:
                            d = r.json()
                            st.session_state.token = d["access_token"]
                            st.session_state.user  = d["user"]
                            refresh_docs()
                            st.rerun()
                        else:
                            st.error(r.json().get("detail", "Invalid credentials."))
                    except Exception:
                        st.error("Backend not reachable. Run: uvicorn backend.main:app --reload --port 8000")

        with tab_up:
            name_rg  = st.text_input("Full name",     key="rg_n", placeholder="Arjun Sharma")
            email_rg = st.text_input("Email address", key="rg_e", placeholder="you@example.com")
            pwd_rg   = st.text_input("Password",      key="rg_p", placeholder="Min 6 characters", type="password")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            if st.button("Create account →", key="btn_rg", use_container_width=True):
                if not name_rg or not email_rg or not pwd_rg:
                    st.error("Please fill in all fields.")
                elif len(pwd_rg) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    try:
                        r = requests.post(f"{BASE_URL}/auth/register",
                                          json={"name": name_rg, "email": email_rg,
                                                "password": pwd_rg}, timeout=15)
                        if r.status_code == 200:
                            d = r.json()
                            st.session_state.token = d["access_token"]
                            st.session_state.user  = d["user"]
                            refresh_docs()
                            st.rerun()
                        else:
                            st.error(r.json().get("detail", "Registration failed."))
                    except Exception:
                        st.error("Backend not reachable.")

        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APP — 2-column stable layout
# ═══════════════════════════════════════════════════════════════════════════════
user      = st.session_state.user or {}
uname     = user.get("name", "User")
uemail    = user.get("email", "")
uinits    = initials(uname)

# Fetch chats
cr    = api_get("/chats")
chats = cr.json() if cr and cr.status_code == 200 else []

# Two columns: sidebar | main
sb_col, main_col = st.columns([0.85, 2.9], gap="small")

# ═══════════════════════════════════════════════════════════════════════════════
# LEFT SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with sb_col:
    # ── Brand ────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="sb-wrap">
      <div class="sb-brand">
        <div class="sb-brand-icon">📄</div>
        <div>
          <div class="sb-brand-name">DocuAssist</div>
          <div class="sb-brand-sub">AI Document Intelligence</div>
        </div>
      </div>
      <div class="sb-label">UPLOAD DOCUMENTS</div>
      <div class="sb-drop">
        <div class="sb-drop-icon">☁</div>
        <div class="sb-drop-txt">Drag &amp; drop your PDF here<br>or <span>browse files</span></div>
      </div>
    """, unsafe_allow_html=True)

    # ── File uploader ─────────────────────────────────────────────────────────
    uploaded = st.file_uploader(
        "Upload PDF", type=["pdf"], accept_multiple_files=True,
        label_visibility="collapsed", key="uploader"
    )
    if uploaded:
        existing = {d["name"] for d in st.session_state.doc_list}
        for uf in uploaded:
            if uf.name not in existing:
                with st.spinner(f"Processing {uf.name}…"):
                    r = api_post("/upload",
                                 files={"file": (uf.name, uf.read(), "application/pdf")})
                    if r and r.status_code == 200:
                        st.success(f"✓ {r.json()['filename']} ready")
                        refresh_docs()
                    else:
                        st.error(f"Failed: {r.json().get('detail','') if r else 'no response'}")

    # ── Uploaded docs ─────────────────────────────────────────────────────────
    if st.session_state.doc_list:
        st.markdown('<div class="sb-label">UPLOADED DOCS</div>', unsafe_allow_html=True)
        for doc in st.session_state.doc_list:
            active = doc["id"] in st.session_state.active_doc_ids
            cls    = "sb-doc on" if active else "sb-doc"
            st.markdown(f"""
            <div class="{cls}">
              <div class="sb-doc-icon">📕</div>
              <div style="flex:1;min-width:0;">
                <div class="sb-doc-name">{doc['name']}</div>
                <div class="sb-doc-meta">{doc.get('pages','?')} pages</div>
              </div>
              <div class="sb-doc-chk">✓</div>
            </div>
            """, unsafe_allow_html=True)
            tog = st.checkbox("", value=active, key=f"chk_{doc['id']}",
                              label_visibility="collapsed")
            if tog and doc["id"] not in st.session_state.active_doc_ids:
                st.session_state.active_doc_ids.append(doc["id"])
                st.rerun()
            elif not tog and doc["id"] in st.session_state.active_doc_ids:
                st.session_state.active_doc_ids.remove(doc["id"])
                st.rerun()

    # ── Conversation history ──────────────────────────────────────────────────
    st.markdown('<div class="sb-label">CONVERSATION HISTORY</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-hist">', unsafe_allow_html=True)

    if chats:
        for chat in chats:
            title  = (chat.get("title") or "New conversation")[:38]
            active = chat["id"] == st.session_state.active_chat_id
            cls    = "sb-hist-item on" if active else "sb-hist-item"
            st.markdown(f"""
            <div class="{cls}">
              <div class="sb-hist-dot"></div>
              <div class="sb-hist-txt">{title}</div>
            </div>
            """, unsafe_allow_html=True)
            c1, c2 = st.columns([6, 1])
            with c1:
                if st.button(title, key=f"ch_{chat['id']}", use_container_width=True):
                    st.session_state.active_chat_id = chat["id"]
                    load_msgs(chat["id"])
                    st.rerun()
            with c2:
                if st.button("×", key=f"dl_{chat['id']}"):
                    api_del(f"/chats/{chat['id']}")
                    if st.session_state.active_chat_id == chat["id"]:
                        st.session_state.active_chat_id = None
                        st.session_state.messages = []
                    st.rerun()
    else:
        st.markdown(
            "<p style='font-size:12px;color:#3a3d50;padding:6px 16px;'>No conversations yet.</p>",
            unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close sb-hist

    # ── User row ──────────────────────────────────────────────────────────────
    st.markdown(f"""
      <div class="sb-user">
        <div class="sb-av">{uinits}</div>
        <div style="flex:1;min-width:0;">
          <div class="sb-uname">{uname}</div>
          <div class="sb-uplan">★ Premium User</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)  # close sb-wrap

    if st.button("Sign out", key="logout", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# RIGHT MAIN AREA
# ═══════════════════════════════════════════════════════════════════════════════
with main_col:
    # ── Topbar ────────────────────────────────────────────────────────────────
    tc1, tc2 = st.columns([3.5, 1])
    with tc1:
        st.markdown("""
        <div class="topbar">
          <div>
            <div class="topbar-title">Document Intelligent Assistant</div>
            <div class="topbar-sub">Ask questions about your documents and get intelligent answers.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with tc2:
        st.markdown("<div style='padding-top:14px;'>", unsafe_allow_html=True)
        if st.button("↗ New Chat", key="new_chat"):
            r = api_post("/chats", json={})
            if r and r.status_code == 200:
                st.session_state.active_chat_id = r.json()["id"]
                st.session_state.messages = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:0;'>",
                unsafe_allow_html=True)

    # ── Messages area ─────────────────────────────────────────────────────────
    msgs = st.session_state.messages

    if not msgs:
        fname = uname.split()[0] if uname else "there"
        st.markdown(f"""
        <div class="empty-state">
          <div class="empty-icon">📄</div>
          <div class="empty-title">Welcome, {fname}</div>
          <div class="empty-sub">
            Upload a PDF from the left panel, then ask any question.<br>
            DocuAssist answers only from your documents — no hallucinations.
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Suggestion chips
        SUGS = [
            "What is the main topic?",
            "Summarize the key points",
            "What are the important dates?",
            "List all conclusions",
        ]
        chip_c = st.columns(2)
        for i, s in enumerate(SUGS):
            with chip_c[i % 2]:
                if st.button(f'"{s}"', key=f"sug_{i}", use_container_width=True):
                    if not st.session_state.active_doc_ids:
                        st.warning("Upload a document first.")
                    else:
                        st.session_state["_pq"] = s
                        st.rerun()
    else:
        # Render messages
        ts = now_ts()
        for msg in msgs:
            role    = msg["role"]
            content = msg.get("content", "")
            sources = msg.get("sources", [])
            if isinstance(sources, str):
                try: sources = json.loads(sources)
                except: sources = []

            if role == "user":
                st.markdown(f"""
                <div class="msg-row-user">
                  <div class="bubble-user">{content}</div>
                  <div class="av-sm">{uinits}</div>
                </div>
                <div class="msg-ts">{ts}</div>
                """, unsafe_allow_html=True)

            else:
                # Format content
                lines = content.split("\n")
                body  = ""
                for ln in lines:
                    ln = ln.strip()
                    if not ln:
                        body += "<div style='height:5px'></div>"
                    elif ln.startswith(("•", "-", "*")):
                        txt = ln.lstrip("•-* ").strip()
                        body += (f"<div style='display:flex;gap:8px;align-items:flex-start;"
                                 f"margin-bottom:4px;'>"
                                 f"<span style='color:#7986cb;flex-shrink:0;margin-top:2px;'>•</span>"
                                 f"<span style='color:#d0d0d8;'>{txt}</span></div>")
                    else:
                        body += f"<div style='color:#d0d0d8;margin-bottom:3px;'>{ln}</div>"

                # Sources
                src_html = ""
                if sources:
                    src_html += "<div class='src-hdr'>📚 Sources</div>"
                    for s in sources[:4]:
                        fn   = s.get("filename", "Document")
                        pg   = s.get("page", "?")
                        prev = s.get("preview", "")[:80]
                        src_html += f"""
                        <div class="src-card">
                          <div class="src-ico">📕</div>
                          <div style="flex:1;min-width:0;">
                            <div class="src-fname">{fn}</div>
                            <div class="src-pg">Page {pg}</div>
                          </div>
                          <div class="src-prev">{prev}</div>
                        </div>"""

                st.markdown(f"""
                <div class="msg-row-bot">
                  <div class="bot-av">🤖</div>
                  <div>
                    <div class="bubble-bot">
                      {body}
                      {src_html}
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Pending suggestion ────────────────────────────────────────────────────
    question = None
    if "_pq" in st.session_state:
        question = st.session_state.pop("_pq")

    # ── Warning ───────────────────────────────────────────────────────────────
    if st.session_state.doc_list and not st.session_state.active_doc_ids:
        st.markdown("""
        <div class="warn-bar">
          <span>⚠</span> No documents selected — tick at least one PDF in the left panel.
        </div>
        """, unsafe_allow_html=True)

    # ── Chat input ────────────────────────────────────────────────────────────
    chat_in = st.chat_input("Ask a question about your documents…", key="ci")
    if chat_in:
        question = chat_in

    if question:
        if not st.session_state.active_doc_ids:
            st.warning("Please upload and select at least one document first.")
        else:
            # Ensure chat session
            if not st.session_state.active_chat_id:
                r = api_post("/chats", json={})
                if r and r.status_code == 200:
                    st.session_state.active_chat_id = r.json()["id"]

            # Save user message
            st.session_state.messages.append(
                {"role": "user", "content": question, "sources": []})

            # Query backend
            with st.spinner("Searching your documents…"):
                r = api_post("/ask", json={
                    "question": question,
                    "doc_ids":  st.session_state.active_doc_ids,
                    "chat_id":  st.session_state.active_chat_id,
                })

            if r and r.status_code == 200:
                d       = r.json()
                answer  = d.get("answer", "No answer returned.")
                sources = d.get("sources", [])
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "sources": sources})
                if d.get("chat_id"):
                    st.session_state.active_chat_id = d["chat_id"]
            else:
                err = r.json().get("detail", "Unknown error") if r else "No response from backend."
                st.session_state.messages.append(
                    {"role": "assistant", "content": f"⚠ {err}", "sources": []})

            st.rerun()
