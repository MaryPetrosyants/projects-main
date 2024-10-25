from fastapi import APIRouter, Depends, Header
from schemas.user import CreateUser
from services.user_manager import UserManager
from repositories.users import Users
from fastapi import Depends
from repositories.auth import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["users"],
)
storage = Users
manager = UserManager(storage)


@router.post("/register/")
def register(user: CreateUser = Depends()):
    return manager.add(user=user)


@router.post("/token")
async def login_for_access_token(email: str, password: str):
    return manager.login(email, password)


@router.get("/current/")
async def read_users_me(Authorization: str = Header(), Refresh_Token: str = Header()):
    user = get_current_user(Authorization, Refresh_Token)
    return user
