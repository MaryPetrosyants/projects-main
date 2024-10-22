from fastapi import APIRouter, Depends
from schemas.user import CreateUser, UserSchema, CurrentUser
from services.user_manager import UserManager
from repositories.users import Users
from schemas.token import Token, TokenData
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from repositories.auth import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token/")

router = APIRouter(
    prefix="/user",
    tags=["users"],
)
storage = Users
manager = UserManager(storage)


@router.post("/register/")
def register(user: CreateUser = Depends()):
    return manager.add(user=user)


@router.post("/token/", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],) -> Token:
    
    return manager.login(username=form_data.username, password=form_data.password)


@router.get("/current/", response_model=UserSchema)
async def read_users_me(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
  
    
    return current_user
