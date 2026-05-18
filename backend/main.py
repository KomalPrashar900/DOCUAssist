# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, upload, query, history, documents
from database import create_tables

app = FastAPI(title='DocuAssist API', version='2.0.0',
              description='AI Document Intelligence — RAG + JWT Auth')

app.add_middleware(CORSMiddleware,
    allow_origins=['http://localhost:8501'],   # Streamlit dev server
    allow_methods=['*'], allow_headers=['*'], allow_credentials=True)

# Public routes (no auth required)
app.include_router(auth.router,      prefix='/api', tags=['Auth'])

# Protected routes (JWT required on every endpoint)
app.include_router(upload.router,    prefix='/api', tags=['Upload'])
app.include_router(query.router,     prefix='/api', tags=['Query'])
app.include_router(history.router,   prefix='/api', tags=['History'])
app.include_router(documents.router, prefix='/api', tags=['Documents'])

@app.on_event('startup')
async def on_startup():
    create_tables()   # creates docuassist.db and all tables on first run

@app.get('/')
def root(): return {'status': 'DocuAssist API running', 'docs': '/docs'}