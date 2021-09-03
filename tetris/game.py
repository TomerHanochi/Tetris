import sys
import pygame as pg

from tetris.utils.assets import Colors, Fonts
from tetris.components.board import Board


class Tetris:
    def __init__(self) -> None:
        pg.init()

        self.__size = self.__w, self.__h = 900, 900
        self.__window = pg.display.set_mode(self.size)

        block_size = 35
        self.__board = Board(block_size)

    def run(self) -> None:
        while True:
            self.window.fill(Colors.black)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.board.draw()

            pg.display.flip()

    @property
    def window(self) -> pg.Surface:
        return self.__window

    @property
    def size(self) -> tuple[int, int]:
        return self.__size

    @property
    def height(self) -> int:
        return self.__h

    @property
    def width(self) -> int:
        return self.__w

    @property
    def board(self) -> Board:
        return self.__board
