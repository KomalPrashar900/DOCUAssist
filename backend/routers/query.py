# backend/routers/query.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from services.auth_service import get_current_user
from services.rag_service import answer_question
from models import Chat, Message
from database import get_db
import json

router = APIRouter()

class QueryReq(BaseModel):                              
    question: str
    doc_ids:  list[str]
    chat_id:  str | None = None

@router.post('/ask')
def ask(
    req: QueryReq,
    current = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current['sub']

    # Create or validate chat session
    if req.chat_id:
        chat = db.query(Chat).filter(Chat.id == req.chat_id,
                                     Chat.user_id == user_id).first()
        if not chat: raise HTTPException(404, 'Chat not found')
    else:
        chat = Chat(user_id=user_id)
        db.add(chat); db.commit(); db.refresh(chat)

    # Run RAG pipeline
    result = answer_question(user_id, req.doc_ids, req.question)

    # Persist both turns to database
    db.add(Message(chat_id=chat.id, role='user',
                   content=req.question, sources='[]'))
    db.add(Message(chat_id=chat.id, role='assistant',
                   content=result['answer'],
                   sources=json.dumps(result['sources'])))

    # Update chat title from first question
    if chat.title == 'New conversation':
        chat.title = req.question[:60]
    db.commit()

    return {**result, 'chat_id': chat.id}