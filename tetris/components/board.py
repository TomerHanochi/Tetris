import pygame as pg

from tetris.utils.assets import Colors


class Board:
    def __init__(self, block_size) -> None:
        self.__size = self.__w, self.__h = 10, 20
        self.__block_size = block_size
        w, h = pg.display.get_window_size()
        self.x = (w - self.block_size * self.w) / 2
        self.y = (h - self.block_size * self.h) / 2
        self.__blocks = []

    def draw(self) -> None:
        for block in self.blocks:
            block.draw()

        for i in range(self.w):
            for j in range(self.h):
                rect = (int(self.block_size * i + self.x), int(self.block_size * j + self.y),
                        self.block_size, self.block_size)
                pg.draw.rect(surface=pg.display.get_surface(), color=Colors.white, rect=rect,
                             width=2)

    @property
    def size(self) -> tuple[int, int]:
        return self.__size

    @property
    def w(self) -> int:
        return self.__w

    @property
    def h(self) -> int:
        return self.__h

    @property
    def blocks(self) -> list:
        return self.__blocks

    @property
    def block_size(self) -> int:
        return self.__block_size
