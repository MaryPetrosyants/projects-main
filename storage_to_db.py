from abc import ABC, abstractmethod


class StorageToDb(ABC):


    @abstractmethod
    def create_table(self):
        pass
