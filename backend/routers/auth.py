# backend/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException,  status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from services.email_service import send_reset_email
from fastapi import status
from services.auth_service import hash_password, verify_password, create_token, get_current_user
from models import User
from database import get_db
import uuid
from datetime import datetime, timedelta, timezone


router = APIRouter()


class RegisterReq(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginReq(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordReq(BaseModel):
    email: EmailStr

class ResetPasswordReq(BaseModel):
    token: str
    new_password: str

@router.post('/auth/register')
def register(req: RegisterReq, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(400, 'Email already registered')
    if len(req.password) < 6:
        raise HTTPException(400, 'Password must be at least 6 characters')

    print("password :",req.password)
    user = User(name=req.name, email=req.email,
                password=hash_password(req.password))
    print("password :",req.password)
    print("hashed password :",user.password)
    db.add(user); 
    db.commit(); 
    db.refresh(user)

    return {
    'access_token': create_token(user.id, user.email),
    'token_type': 'bearer',
    'user': {
        'id': user.id,
        'name': user.name,
        'email': user.email,
    },
}       

@router.post('/auth/login')
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()
 
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
 
    token = create_token(user_id=str(user.id), email=user.email)
 
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,   # FIX: name included
            "email": user.email,
        },
    }

@router.get('/auth/me')
def me(
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # print("CURRENT USER =", current)

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

# ── Forgot password ───────────────────────────────────────────────────────────

@router.post('/auth/forgot-password')
def forgot_password(req: ForgotPasswordReq, db: Session = Depends(get_db)):
    """
    Generate a 15-minute reset token and email it to the user.
    Always returns 200 to avoid leaking whether an email exists.
    """
    user = db.query(User).filter(User.email == req.email).first()
    if user:
        token = str(uuid.uuid4())
        exp   = datetime.now(timezone.utc) + timedelta(minutes=15)

        user.reset_token     = token
        user.reset_token_exp = exp
        db.commit()

        send_reset_email(
            to_email=user.email,
            reset_token=token,
            user_name=user.name,
        )

    return {'message': 'If an account with that email exists, a reset link has been sent.'}


# ── Reset password ────────────────────────────────────────────────────────────

@router.post('/auth/reset-password')
def reset_password(req: ResetPasswordReq, db: Session = Depends(get_db)):
    """Validate the reset token and update the password."""
    if len(req.new_password) < 6:
        raise HTTPException(400, 'Password must be at least 6 characters')

    user = db.query(User).filter(User.reset_token == req.token).first()

    if not user:
        raise HTTPException(400, 'Invalid or expired reset link')

    # Check expiry
    exp = user.reset_token_exp
    if exp is None:
        raise HTTPException(400, 'Invalid reset link')

    # Make exp timezone-aware if it's naive
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)

    if datetime.now(timezone.utc) > exp:
        raise HTTPException(400, 'Reset link has expired. Please request a new one.')

    user.password        = hash_password(req.new_password)
    user.reset_token     = None
    user.reset_token_exp = None
    db.commit()

    return {'message': 'Password updated successfully. You can now sign in.'}


