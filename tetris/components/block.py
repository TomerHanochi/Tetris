import pygame as pg


class Block:
    def __init__(self, x: int, y: int, w: int, h: int, color: tuple[int, int, int]) -> None:
        self.__rect = pg.Rect(x, y, w, h)
        self.__color = color

    def draw(self) -> None:
        pg.draw.rect(pg.display.get_surface(), self.color, self.rect, 0)

    @property
    def color(self) -> tuple[int, int, int]:
        return self.__color

    @property
    def rect(self) -> pg.Rect:
        return self.__rect
