from abc import ABC, abstractmethod
from repositories.storage import Storage


class UserStorage(Storage):

    @abstractmethod
    def login():
        pass
