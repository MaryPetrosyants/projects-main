from datetime import datetime, timedelta, timezone
from typing import Annotated
from jwt.exceptions import InvalidTokenError
import jwt
from fastapi import APIRouter, Depends, Request
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from schemas.token import TokenData
from config.database import get_db
from models.user import User
from typing import Union, Any
from config.config import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,JWT_REFRESH_SECRET_KEY,REFRESH_TOKEN_EXPIRE_MINUTES



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token/")

router = APIRouter()

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
        timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": user.email,
        "exp": expire,
    }
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user: User = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception

    return user
