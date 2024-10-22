from abc import ABC, abstractmethod


class Storage(ABC):

   
    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def delete(self, id: str):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def get_list(self):
        pass
