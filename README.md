# DOCUAssist
# DocuAssist — Fixed & Working

## What Was Fixed

| # | File | Fix |
|---|------|-----|
| 1 | `frontend/app/src/App.jsx` | **Added `apiFetch` helper** — it was missing, causing blank screen after login |
| 2 | `frontend/app/src/App.jsx` | **JWT persisted** to `localStorage` — no re-login on refresh |
| 3 | `frontend/app/src/App.jsx` | **Chat history** loads correctly when selecting a conversation |
| 4 | `frontend/app/src/App.jsx` | **Document selection** with All/None toggle controls |
| 5 | `frontend/app/src/App.jsx` | **Responsive UI** — mobile sidebar with hamburger menu |
| 6 | `backend/routers/auth.py` | Login response now includes `name` field (was missing) |
| 7 | `backend/database.py` | Added `dotenv` load + fallback `DATABASE_URL` (was crashing if `.env` missing) |
| 8 | `backend/services/auth_service.py` | Env vars have safe defaults, won't crash on missing `.env` |
| 9 | `backend/services/rag_service.py` | Env vars have safe defaults |
| 10 | `backend/.env` | **Created `.env`** with all required config (was missing) |

---

## Setup

### 1. Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Edit .env — add your Google API key
nano .env                         # set GOOGLE_API_KEY=your-key

# Run
uvicorn main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend/app

npm install
npm run dev
```

Open: http://localhost:5173

---

## Environment Variables (backend/.env)

```env
DATABASE_URL=sqlite:///./docuassist.db
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
TOKEN_EXPIRE_HOURS=24
UPLOAD_DIR=./uploads
FAISS_INDEX_DIR=./faiss_index
GOOGLE_API_KEY=your-google-api-key-here
LLM_MODEL=gemini-1.5-flash
CHUNK_SIZE=800
CHUNK_OVERLAP=100
```

Get a free Google API key at: https://aistudio.google.com/app/apikey

---

## Flow

1. Register / Login → JWT issued
2. Upload PDF → text extracted, chunked, embedded into FAISS index
3. Ask question → RAG retrieves relevant chunks → Gemini generates answer
4. Chat history saved to SQLite, persisted across sessions