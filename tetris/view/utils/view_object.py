from abc import ABC, abstractmethod


class ViewObject(ABC):
    """ An abstract class representing a gui object. """
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass
