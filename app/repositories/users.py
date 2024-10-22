from fastapi import HTTPException, status
from schemas.user import CreateUser
from config.database import get_db
from passlib.context import CryptContext
from models.user import User
from repositories.user_storage import UserStorage
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from models.user import User
from schemas.token import Token
from repositories.auth import create_access_token, authenticate_user, create_access_token



class Users(UserStorage):

    def add(user: CreateUser):
        db = next(get_db())
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hash_pass = pwd_context.hash(user.password)
        db_user = User(name=user.name, email=user.email, password=hash_pass)
        db.add(db_user)
        db.commit()

    def delete():
        pass

    def update():
        pass

    def get_list():
        pass

    def login(email, password):
        user = authenticate_user(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(user)
        return Token(access_token=access_token, token_type="bearer")
