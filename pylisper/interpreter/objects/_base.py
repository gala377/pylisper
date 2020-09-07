from abc import ABC, abstractmethod


class BaseObject(ABC):
    @abstractmethod
    def __str__(self):
        ...
