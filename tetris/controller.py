import sys
import pygame as pg

from tetris.model import Model
from tetris.view import View


class Controller:
    def __init__(self) -> None:
        self.__model = Model()
        self.__view = View(self.__model)

    def handle(self, event) -> None:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                self.__model.move_tetromino_right()
            elif event.key == pg.K_LEFT:
                self.__model.move_tetromino_left()
            elif event.key == pg.K_UP or event.key == pg.K_x:
                self.__model.rotate_tetromino_right()
            elif event.key == pg.KMOD_CTRL or event.key == pg.K_z:
                self.__model.rotate_tetromino_left()
            elif event.key == pg.K_DOWN:
                # TODO soft drop
                pass
            elif event.key == pg.K_SPACE:
                self.__model.drop_tetromino()
            elif event.key == pg.KMOD_SHIFT or event.key == pg.K_c:
                self.__model.hold()
        elif event.type == pg.KEYUP:
            # TODO keyup
            if event.key == pg.K_RIGHT:
                pass
            elif event.key == pg.K_LEFT:
                pass
            elif event.key == pg.K_DOWN:
                pass

    def run(self) -> None:
        while True:
            for event in pg.event.get():
                self.handle(event)

            self.__view.update()

    @property
    def model(self) -> Model:
        return self.__model
