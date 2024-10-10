from abc import ABC, abstractmethod


class Storage(ABC):

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def get_list(self):
        pass
