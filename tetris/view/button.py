import pygame as pg

from tetris.assets.assets import Colors, Fonts


class Button:
    def __init__(self, x: int, y: int, text: str, function) -> None:
        self.__text = Fonts.button.render(text, True, Colors.button_text,
                                          Colors.button_background)
        self.__x, self.__y = x, y
        self.__w, self.__h = self.__text.get_width(), self.__text.get_height()
        self.__function = function

    @property
    def is_clicked(self) -> bool:
        x, y = pg.mouse.get_pos()
        return 0 < x - self.__x < self.__w and 0 < y - self.__y < self.__h

    def click(self) -> None:
        self.__function()

    def draw(self, window: pg.Surface) -> None:
        window.fill(Colors.button_background, (self.__x - self.__w * 0.05,
                                               self.__y - self.__h * 0.05,
                                               self.__w * 1.1, self.__h * 1.1))
        window.blit(self.__text, (self.__x, self.__y))
