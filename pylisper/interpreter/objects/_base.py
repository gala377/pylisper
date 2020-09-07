from abc import ABC, abstractmethod


class BaseObject(ABC):
    """
    Base class for all of the deriving objects.

    For now it doesn't provide much functionality beside
    assuring that all of the objects have a reasonable
    string representation and having all of them
    have distinct root.
    """

    @abstractmethod
    def __str__(self):
        ...
