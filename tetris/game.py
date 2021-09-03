import sys
import pygame as pg

from tetris.utils.colors import Colors


class Tetris:
    def __init__(self) -> None:
        pg.init()

        self.__size = self.__width, self.__height = 900, 900
        self.__window = pg.display.set_mode(self.size)

    @property
    def window(self) -> pg.Surface:
        return self.__window

    @property
    def size(self) -> tuple[int, int]:
        return self.__size

    @property
    def height(self) -> int:
        return self.__height

    @property
    def width(self) -> int:
        return self.__width

    def run(self) -> None:
        while True:
            self.window.fill(Colors.black)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            pg.display.flip()
