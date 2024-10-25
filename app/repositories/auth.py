from datetime import datetime, timedelta, timezone
from typing import Annotated
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import jwt
from fastapi import APIRouter, Depends, Request, Header
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from schemas.token import TokenData
from config.database import get_db
from models.user import User
from typing import Union, Any
from config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, JWT_REFRESH_SECRET_KEY, REFRESH_TOKEN_EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(email: str) -> User | None:
    db = next(get_db())
    user = db.query(User).filter(User.email == email).one_or_none()
    return user


def authenticate_user(email: str, password: str) -> User | None:
    user = get_user(email)
    if not user or not pwd_context.verify(password, user.password):
        return False
    return user


def create_access_token(user: User) -> str:

    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {
        "sub": user.email,
        "exp": expire,
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(user: User) -> str:
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=int(REFRESH_TOKEN_EXPIRE_MINUTES))
    to_encode = {
        "sub": user.email,
        "exp": expire,
    }
    encoded_jwt = jwt.encode(
        to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(acc_token, ref_token) -> User | str:
    try:
        payload = jwt.decode(acc_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_data = TokenData(email=email)
        user: User = get_user(email=token_data.email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except jwt.exceptions.ExpiredSignatureError:
        return refresh_token(ref_token)
    return user


def refresh_token(ref_token) -> str:
    try:
        payload = jwt.decode(
            ref_token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_data = TokenData(email=email)
        user: User = get_user(email=token_data.email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if user.refresh_token == ref_token:
            new_acc_token = create_access_token(user)
            return new_acc_token
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
def get_heder(Authorization: str = Header(), Refresh_Token: str=Header()):
    print(Authorization, Refresh_Token)
    current_user = get_current_user(Authorization, Refresh_Token)
    return {"current_user": current_user}

def protected(func):
    def wrapper(*args, **kwargs):
        Authorization = kwargs.get("Authorization")
        Refresh_Token = kwargs.get("Refresh_Token")
        print(Authorization, Refresh_Token)
        func(*args, **kwargs)
    return wrapper  

