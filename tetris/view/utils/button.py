from typing import Callable

import pygame as pg

from tetris.assets.assets import Colors, Fonts
from tetris.view.utils.view_object import ViewObject
from tetris.view.utils.draw import Draw


class Button(ViewObject):
    def __init__(self, x: float, y: float, text: str, func: Callable) -> None:
        self.__text = Fonts.button.render(text, True, Colors.button_text,
                                          Colors.button_background)
        self.__x = x
        self.__y = y
        self.__w = self.__text.get_width()
        self.__h = self.__text.get_height()
        self.func = func

    @property
    def is_clicked(self) -> bool:
        x, y = pg.mouse.get_pos()
        return 0 < x - self.__x < self.__w and 0 < y - self.__y < self.__h

    def click(self, *args) -> None:
        self.func(*args)

    def draw(self) -> None:
        # the offset is to make sure the background is bigger than the text
        offset = 0.05
        Draw.fill(x=self.__x - self.__w * offset, y=self.__y - self.__h * offset,
                  w=self.__w * (1 + offset * 2), h=self.__h * (1 + offset * 2),
                  color=Colors.button_background)
        Draw.image(self.__x, self.__y, self.__text)

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def w(self) -> int:
        return self.__w

    @property
    def h(self) -> int:
        return self.__h
