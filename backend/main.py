# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, upload, query, history, documents
from database import create_tables

app = FastAPI(title='DocuAssist API', version='2.0.0',
              description='AI Document Intelligence — RAG + JWT Auth')
print("this is first step:",app)
   
    
app.add_middleware(CORSMiddleware,                           
    allow_origins=['http://localhost:5173'],   # React dev server   
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True)     
print("this is second step:",app)

# Public routes (no auth required)
app.include_router(auth.router,      prefix='/api', tags=['Auth'])  

# Protected routes (JWT required on every endpoint)        
app.include_router(upload.router,    prefix='/api', tags=['Upload'])
app.include_router(query.router,     prefix='/api', tags=['Query'])
app.include_router(history.router,   prefix='/api', tags=['History'])
app.include_router(documents.router, prefix='/api', tags=['Documents'])
print("this is third step:",app)

@app.on_event('startup')
async def on_startup():
    create_tables()   # creates docuassist.db and all tables on first run
    print("database setup")

@app.get('/')
def root(): return {'status': 'DocuAssist API running', 'docs': '/docs'}   
print("this is fifth step:",app)

