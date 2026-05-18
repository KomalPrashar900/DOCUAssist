# backend/services/auth_service.py
"""from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY          = os.getenv('SECRET_KEY')
ALGORITHM           = os.getenv('ALGORITHM')
TOKEN_EXPIRE_HOURS  = int(os.getenv('TOKEN_EXPIRE_HOURS'))

pwd_ctx  = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2   = OAuth2PasswordBearer(tokenUrl='/api/auth/login')

def hash_password(plain: str) -> str:
    return pwd_ctx.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

def create_token(user_id: str, email: str) -> str:
    exp = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    return jwt.encode({'sub': user_id, 'email': email, 'exp': exp},
                      SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid or expired token')

async def get_current_user(token: str = Depends(oauth2)) -> dict:
    print("TOKEN =", token)
    return decode_token(token)  # returns {'sub': user_id, 'email': ...}"""

 # backend/services/auth_service.py

from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRE_HOURS = int(os.getenv("TOKEN_EXPIRE_HOURS"))

pwd_ctx = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)


def hash_password(plain: str) -> str:
    return pwd_ctx.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)


def create_token(user_id: str, email: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(
        hours=TOKEN_EXPIRE_HOURS
    )

    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": exp
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


async def get_current_user(
    token: str = Depends(oauth2)
) -> dict:

    print("TOKEN =", token)

    return decode_token(token)