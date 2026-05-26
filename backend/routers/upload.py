# backend/routers/upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from services.auth_service import get_current_user
from services.pdf_service import extract_text_from_pdf
from services.rag_service import ingest_document
from models import Document
from database import get_db
import aiofiles, os, uuid
from dotenv import load_dotenv

load_dotenv()   

router  = APIRouter()
UPLOAD  = os.getenv('UPLOAD_DIR')

@router.post('/upload')
async def upload_pdf(
    file: UploadFile = File(...),
    current = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, 'Only PDF files accepted')

    user_id  = current['sub']
    doc_id   = str(uuid.uuid4())
    user_dir = os.path.join(UPLOAD, user_id)
    os.makedirs(user_dir, exist_ok=True)
    file_path = os.path.join(user_dir, f'{doc_id}.pdf')

    try:
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(await file.read())

        pages  = extract_text_from_pdf(file_path)
        chunks = ingest_document(user_id, doc_id, file.filename, pages)

        doc_row = Document(id=doc_id, user_id=user_id,
                           name=file.filename, file_path=file_path,
                           pages=str(len(pages)), chunks=str(chunks))
        db.add(doc_row); db.commit()

        return {
            "doc_id": doc_id,
            "name": file.filename,
            "filename": file.filename,
            "pages": len(pages),
            "chunks": chunks,
            "status": "ready"
        }

    except Exception as e:
        if os.path.exists(file_path): os.remove(file_path)
        raise HTTPException(500, f'Processing failed: {str(e)}')