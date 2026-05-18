# backend/routers/history.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.auth_service import get_current_user
from models import Chat, Message
from database import get_db
import json

router = APIRouter()

@router.get('/chats')
def list_chats(current=Depends(get_current_user), db: Session=Depends(get_db)):
    chats = (db.query(Chat)
               .filter(Chat.user_id == current['sub'])
               .order_by(Chat.created_at.desc())
               .all())
    return [{'id': c.id, 'title': c.title, 'created_at': str(c.created_at)}
            for c in chats]

@router.post('/chats')
def create_chat(current=Depends(get_current_user), db: Session=Depends(get_db)):
    chat = Chat(user_id=current['sub'])
    db.add(chat); db.commit(); db.refresh(chat)
    return {'id': chat.id, 'title': chat.title}

@router.get('/chats/{chat_id}/messages')
def get_messages(chat_id: str, current=Depends(get_current_user),
                 db: Session=Depends(get_db)):
    msgs = (db.query(Message)
              .filter(Message.chat_id == chat_id)
              .order_by(Message.created_at)
              .all())
    return [{'id': m.id, 'role': m.role, 'content': m.content,
             'sources': json.loads(m.sources)} for m in msgs]

@router.delete('/chats/{chat_id}')
def delete_chat(chat_id: str, current=Depends(get_current_user),
                db: Session=Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id,
                                 Chat.user_id == current['sub']).first()
    if not chat: raise HTTPException(404, 'Chat not found')
    db.query(Message).filter(Message.chat_id == chat_id).delete()
    db.delete(chat); db.commit()
    return {'status': 'deleted'}