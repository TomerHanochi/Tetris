import sys
import pygame as pg

from tetris.model import Model
from tetris.view import View


class Controller:
    def __init__(self) -> None:
        self.__model = Model()
        self.__view = View(self)
        self.dt = 0
        self.__fps = 10
        self.__fps_clock = pg.time.Clock()

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
                pass
            elif event.key == pg.K_SPACE:
                self.__model.drop_tetromino()
            elif event.key == pg.KMOD_SHIFT or event.key == pg.K_c:
                pass

    def run(self) -> None:
        while True:
            for event in pg.event.get():
                self.handle(event)

            self.__model.update(self.dt)

            self.__view.update()

            # Makes sure the game runs at a stable fps
            # on every computer
            self.dt = self.__fps_clock.tick(self.__fps)

    @property
    def model(self) -> Model:
        return self.__model
