# backend/routers/documents.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.auth_service import get_current_user
from models import Document
from database import get_db

router = APIRouter()

@router.get('/documents')
def list_documents(current=Depends(get_current_user),
                   db: Session=Depends(get_db)):
    docs = (db.query(Document)
              .filter(Document.user_id == current['sub'])
              .order_by(Document.created_at.desc())
              .all())
    return [{'id': d.id, 'name': d.name,
             'pages': d.pages, 'chunks': d.chunks} for d in docs]

@router.delete('/documents/{doc_id}')
def delete_document(doc_id: str,
                    current=Depends(get_current_user),   
                    db: Session=Depends(get_db)):
    import os, shutil
    doc = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == current['sub']
    ).first()
    if not doc: return {'status': 'not found'}

    # Remove PDF file
    if os.path.exists(doc.file_path):
        os.remove(doc.file_path)

    # Remove FAISS index
    faiss_path = f'./faiss_index/{current["sub"]}/{doc_id}'
    if os.path.exists(faiss_path):
        shutil.rmtree(faiss_path)

    db.delete(doc); db.commit()
    return {'status': 'deleted'}