from abc import ABC, abstractmethod


class ViewObject(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass
