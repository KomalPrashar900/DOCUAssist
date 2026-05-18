# frontend/app.py — Complete DocuAssist Streamlit Application
import streamlit as st
import requests, json, os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv('BACKEND_URL', 'http://localhost:8000/api')

# ── Page config ─────────────────────────────────────────────────────
st.set_page_config(
    page_title='DocuAssist',
    page_icon='📄',
    layout='wide',
    initial_sidebar_state='expanded'
)

# ── Custom CSS — hide Streamlit UI chrome, style chat ────────────────
st.markdown('''<style>
  #MainMenu, footer, .stDeployButton { visibility: hidden; }
  .stButton > button {
    border-radius: 8px; font-weight: 500;
    transition: all .2s;
  }
  .stTextInput > div > input {
    border-radius: 8px;
  }
  /* Sidebar width */
  section[data-testid='stSidebar'] { width: 280px !important; }
  /* Chat input */
  .stChatInput textarea { border-radius: 12px !important; }
</style>''', unsafe_allow_html=True)

# ── Session state initialisation ────────────────────────────────────
defaults = {
    'token': None, 'user': None,
    'active_chat_id': None, 'messages': [],
    'active_doc_ids': [], 'doc_list': []
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Helpers ─────────────────────────────────────────────────────────
def headers():
    return {'Authorization': f'Bearer {st.session_state.token}'}

def api_get(path):
    return requests.get(f'{BASE_URL}{path}', headers=headers())

def api_post(path, **kwargs):
    return requests.post(f'{BASE_URL}{path}', headers=headers(), **kwargs)

def api_delete(path):
    return requests.delete(f'{BASE_URL}{path}', headers=headers())

def refresh_docs():
    r = api_get('/documents')
    if r.status_code == 200:
        st.session_state.doc_list = r.json()
        st.session_state.active_doc_ids = [d['id'] for d in r.json()]

# ═══════════════════════════════════════════════════════════════════
# AUTH SCREEN — shown when not logged in
# ═══════════════════════════════════════════════════════════════════
if not st.session_state.token:
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.image('logo.png', width=260)  # DocuAssist logo
        st.markdown('### Welcome back')
        st.caption('Sign in to your account to continue')
        st.divider()

        tab_login, tab_reg = st.tabs(['Sign in', 'Create account'])

        with tab_login:
            email = st.text_input('Email address', key='li_email',
                                  placeholder='you@example.com')
            pwd   = st.text_input('Password', type='password', key='li_pwd')
            if st.button('Sign in', use_container_width=True, type='primary'):
                r = requests.post(f'{BASE_URL}/auth/login',
                                  json={'email': email, 'password': pwd})
                if r.status_code == 200:
                    data = r.json()
                    st.session_state.token = data['token']
                    st.session_state.user  = data['user']
                    refresh_docs()
                    st.rerun()
                else:
                    st.error(r.json().get('detail', 'Login failed'))

        with tab_reg:
            name  = st.text_input('Full name', key='rg_name')
            email = st.text_input('Email', key='rg_email')
            pwd   = st.text_input('Password (min 6 chars)',
                                  type='password', key='rg_pwd')
            if st.button('Create account', use_container_width=True, type='primary'):
                r = requests.post(f'{BASE_URL}/auth/register',
                                  json={'name': name, 'email': email, 'password': pwd})
                if r.status_code == 200:
                    data = r.json()
                    st.session_state.token = data['token']
                    st.session_state.user  = data['user']
                    refresh_docs()
                    st.rerun()
                else:
                    st.error(r.json().get('detail', 'Registration failed'))
    st.stop()

# ═══════════════════════════════════════════════════════════════════
# SIDEBAR — ChatGPT-style conversation history + user profile
# ═══════════════════════════════════════════════════════════════════
with st.sidebar:
    # New chat button at top
    if st.button('+ New conversation', use_container_width=True):
        r = api_post('/chats', json={})
        if r.status_code == 200:
            st.session_state.active_chat_id = r.json()['id']
            st.session_state.messages = []
        st.rerun()

    st.divider()

    # Chat history list
    chats_r = api_get('/chats')
    if chats_r.status_code == 200:
        chats = chats_r.json()
        if chats:
            st.caption('CONVERSATIONS')
            for chat in chats:
                col_btn, col_del = st.columns([5, 1])
                label = (chat['title'][:34] + '...'
                         if len(chat['title']) > 34 else chat['title'])
                with col_btn:
                    is_active = chat['id'] == st.session_state.active_chat_id
                    if st.button(
                        label,
                        key=f'chat_{chat["id"]}',
                        use_container_width=True,
                        type='primary' if is_active else 'secondary'
                    ):
                        st.session_state.active_chat_id = chat['id']
                        msgs_r = api_get(f'/chats/{chat["id"]}/messages')
                        st.session_state.messages = (
                            msgs_r.json() if msgs_r.status_code == 200 else []
                        )
                        st.rerun()
                with col_del:
                    if st.button('×', key=f'del_{chat["id"]}',
                                 help='Delete conversation'):
                        api_delete(f'/chats/{chat["id"]}')
                        if st.session_state.active_chat_id == chat['id']:
                            st.session_state.active_chat_id = None
                            st.session_state.messages = []
                        st.rerun()
        else:
            st.caption('No conversations yet')
            st.caption('Upload a PDF and start asking questions')

    # User profile at bottom
    st.divider()
    user = st.session_state.user or {}
    name = user.get('name', 'User')
    initials = ''.join(w[0].upper() for w in name.split()[:2])
    st.markdown(f'**{name}**')
    st.caption(user.get('email', ''))
    if st.button('Sign out', use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ═══════════════════════════════════════════════════════════════════
# MAIN AREA — header, upload, chat
# ═══════════════════════════════════════════════════════════════════
st.markdown('## Document Intelligent Assistant')
st.caption('Ask questions about your documents — answers are sourced exclusively from your PDFs')
st.divider()

# ── PDF Upload expander ──────────────────────────────────────────────
docs_loaded = len(st.session_state.doc_list) > 0
with st.expander(
    f'Upload Documents ({len(st.session_state.doc_list)} loaded)',
    expanded=not docs_loaded
):
    uploaded = st.file_uploader(
        'Drag & drop PDFs here or click to browse',
        type=['pdf'],
        accept_multiple_files=True,
        label_visibility='collapsed'
    )
    if uploaded:
        for uf in uploaded:
            already = [d['name'] for d in st.session_state.doc_list]
            if uf.name not in already:
                with st.spinner(f'Processing {uf.name}...'):
                    r = api_post('/upload',
                                 files={'file': (uf.name, uf.read(), 'application/pdf')})
                    if r.status_code == 200:
                        d = r.json()
                        st.success(f'Ready: {d["filename"]} — {d["pages"]} pages, {d["chunks"]} chunks indexed')
                        refresh_docs()
                    else:
                        st.error(f'Failed: {r.json().get("detail", "Unknown error")}')

    # Show currently loaded documents with checkboxes
    if st.session_state.doc_list:
        st.markdown('**Active documents (checked = included in search):**')
        new_active = []
        for doc in st.session_state.doc_list:
            is_on = doc['id'] in st.session_state.active_doc_ids
            if st.checkbox(
                f'{doc["name"]}  —  {doc["pages"]} pages',
                value=is_on,
                key=f'chk_{doc["id"]}'
            ):
                new_active.append(doc['id'])
        st.session_state.active_doc_ids = new_active

# ── Chat history display ─────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])
        if msg['role'] == 'assistant' and msg.get('sources'):
            with st.expander(f'Sources ({len(msg["sources"])})'):
                for src in msg['sources']:
                    cols = st.columns([3, 1])
                    cols[0].markdown(f'**{src["filename"]}**')
                    cols[1].markdown(f'Page **{src["page"]}**')
                    st.caption(src.get('preview', ''))
                    st.divider()

# ── Warning when no docs selected ───────────────────────────────────
if not st.session_state.active_doc_ids and st.session_state.doc_list:
    st.warning('No documents selected. Check at least one document above.')

# ── Chat input ───────────────────────────────────────────────────────
if question := st.chat_input('Ask a question about your documents...'):
    if not st.session_state.active_doc_ids:
        st.warning('Please upload and select at least one document first.')
        st.stop()

    # Ensure a chat session exists
    if not st.session_state.active_chat_id:
        r = api_post('/chats', json={})
        st.session_state.active_chat_id = r.json()['id']

    # Show user message
    with st.chat_message('user'):
        st.markdown(question)
    st.session_state.messages.append({'role': 'user', 'content': question, 'sources': []})

    # Query RAG pipeline
    with st.chat_message('assistant'):
        with st.spinner('Searching your documents...'):
            r = api_post('/ask', json={
                'question': question,
                'doc_ids':  st.session_state.active_doc_ids,
                'chat_id':  st.session_state.active_chat_id
            })

        if r.status_code == 200:
            data = r.json()
            st.markdown(data['answer'])
            if data.get('sources'):
                with st.expander(f'Sources ({len(data["sources"])})'):
                    for src in data['sources']:
                        cols = st.columns([3, 1])
                        cols[0].markdown(f'**{src["filename"]}**')
                        cols[1].markdown(f'Page **{src["page"]}**')
                        st.caption(src.get('preview', ''))
                        st.divider()
            st.session_state.messages.append({
                'role': 'assistant',
                'content': data['answer'],
                'sources': data.get('sources', [])
            })
            if data.get('chat_id'):
                st.session_state.active_chat_id = data['chat_id']
        else:
            st.error('Query failed. Check that the backend is running.')