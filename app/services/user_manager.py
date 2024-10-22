
from repositories.user_storage import UserStorage
from schemas.user import CreateUser
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserManager:
    def __init__(self, storage: UserStorage) -> None:
        self.storage = storage

    def add(self, user: CreateUser) -> None:

        return self.storage.add(user)

    def login(self, username, password):

        return self.storage.login(username, password)
