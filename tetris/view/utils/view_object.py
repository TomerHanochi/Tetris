from abc import ABC, abstractmethod

from tetris.controller.view_info import ViewInfo


class ViewObject(ABC):
    """ An abstract class representing a gui object. """

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def draw(self, view_info: ViewInfo) -> None:
        pass
