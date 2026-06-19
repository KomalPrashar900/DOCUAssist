# backend/models.py
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Boolean
from database import Base
from datetime import datetime
import uuid

def gen_id(): return str(uuid.uuid4())

class User(Base):
    __tablename__ = 'users'
    id              = Column(String, primary_key=True, default=gen_id)  
    email           = Column(String, unique=True, nullable=False, index=True)
    name            = Column(String, nullable=False)
    password        = Column(String, nullable=False)        # bcrypt hash
    created_at      = Column(DateTime, default=datetime.utcnow)
    reset_token     = Column(String, nullable=True)                     # password-reset token
    reset_token_exp = Column(DateTime, nullable=True)       # expiry (15 min)

class Chat(Base):
    __tablename__ = 'chats'
    id         = Column(String, primary_key=True, default=gen_id)
    user_id    = Column(String, ForeignKey('users.id'), nullable=False, index=True)
    title      = Column(String, default='New conversation')
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = 'messages'
    id         = Column(String, primary_key=True, default=gen_id)
    chat_id    = Column(String, ForeignKey('chats.id'), nullable=False, index=True)
    role       = Column(String, nullable=False)         # 'user' or 'assistant'
    content    = Column(Text, nullable=False)
    sources    = Column(Text, default='[]')             # JSON array of citations
    created_at = Column(DateTime, default=datetime.utcnow)

class Document(Base):
    __tablename__ = 'documents'
    id         = Column(String, primary_key=True, default=gen_id)
    user_id    = Column(String, ForeignKey('users.id'), nullable=False, index=True)
    name       = Column(String, nullable=False)         # original filename
    file_path  = Column(String, nullable=False)         # path on disk
    pages      = Column(String, default='0')
    chunks     = Column(String, default='0')
    created_at = Column(DateTime, default=datetime.utcnow)
