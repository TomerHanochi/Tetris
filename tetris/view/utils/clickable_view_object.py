from abc import abstractmethod

from tetris.view.utils.view_object import ViewObject


class ClickableViewObject(ViewObject):
    """ An abstract class representing a clickable gui object. """

    @abstractmethod
    def is_clicked(self) -> bool:
        pass

    @abstractmethod
    def click(self) -> bool:
        pass
