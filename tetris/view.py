import pygame as pg

from tetris.utils.consts import Consts
from tetris.assets.assets import Colors
from tetris.model import Model


class View:
    def __init__(self, controller) -> None:
        self.__window = pg.display.set_mode(Consts.SCREEN_SIZE)
        self.__model = Model()
        self.__controller = controller

    def update(self) -> None:
        self.__window.fill(Colors.black)

        for event in pg.event.get():
            self.__controller.handle(event.type)

        pg.display.flip()
