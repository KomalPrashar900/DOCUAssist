# backend/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from streamlit import status, user
from services.auth_service import hash_password, verify_password, create_token, get_current_user
from models import User
from database import get_db


router = APIRouter()


class RegisterReq(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginReq(BaseModel):
    email: EmailStr
    password: str

@router.post('/auth/register')
def register(req: RegisterReq, db: Session = Depends(get_db)):
    print(type(req.password))
    print(type(req.password))
    print(len(req.password))
    print(repr(req.password))
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(400, 'Email already registered')
    if len(req.password) < 6:
        raise HTTPException(400, 'Password must be at least 6 characters')

    user = User(name=req.name, email=req.email,
                password=hash_password(req.password))
    
    db.add(user); db.commit(); db.refresh(user)
    return {'token': create_token(user.id, user.email),
            'user': {'id': user.id, 'name': user.name, 'email': user.email}}


@router.post('/auth/login')
# def login(req: LoginReq, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == req.email).first()
#     if not user or not verify_password(req.password, user.password):
#         raise HTTPException(401, 'Invalid email or password')
#     return {'token': create_token(user.id, user.email),
#             'user': {'id': user.id, 'name': user.name, 'email': user.email}}
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    email = form_data.username
    password = form_data.password

    print("LOGIN:", email)

    # Find user by email
    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create token with REAL user id
    token = create_token(
        user_id=str(user.id),
        email=user.email
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get('/auth/me')
# def me(current=Depends(get_current_user), db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == current['sub']).first()
#     if not user: raise HTTPException(404, 'User not found')
#     return {'id': user.id, 'name': user.name, 'email': user.email}
def me(
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print("CURRENT USER =", current)

    user = db.query(User).filter(
        User.id == current["sub"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }