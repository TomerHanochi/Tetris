import sys
import pygame as pg

from tetris.model import Model
from tetris.view import View


class Controller:
    def __init__(self) -> None:
        self.__model = Model()
        self.__view = View(self)

    def handle(self, event) -> None:
        if event == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event == pg.K_RIGHT:
            pass
        elif event == pg.K_LEFT:
            pass
        elif event == pg.K_UP or event == pg.K_x:
            pass
        elif event == pg.KMOD_CTRL or event == pg.K_z:
            pass
        elif event == pg.K_DOWN:
            pass
        elif event == pg.K_SPACE:
            pass
        elif event == pg.KMOD_SHIFT or event == pg.K_c:
            pass

    def run(self) -> None:
        while True:
            self.__model.update()
            self.__view.update()

    @property
    def model(self) -> Model:
        return self.__model
