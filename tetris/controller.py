import sys

import pygame as pg

from tetris.model.model import Model
from tetris.view.view import View


class Controller:
    """
    Handles all user input and the main loop of the game
    Controls both the view and the model
    """
    def __init__(self) -> None:
        self.__model = Model()
        self.__view = View(self.__model)

    def handle(self, event) -> None:
        """Handles the various pygame events"""
        if event.type == pg.QUIT:
            # if the close window button was clicked
            # update the high score and quit
            self.__model.set_high_score()
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                self.__model.start_move_right()
            elif event.key == pg.K_LEFT:
                self.__model.start_move_left()
            elif event.key == pg.K_UP or event.key == pg.K_x:
                self.__model.rotate_right()
            elif event.key == pg.KMOD_CTRL or event.key == pg.K_z:
                self.__model.rotate_left()
            elif event.key == pg.K_DOWN:
                self.__model.start_soft_drop()
            elif event.key == pg.K_SPACE:
                self.__model.hard_drop()
            elif event.key == pg.KMOD_SHIFT or event.key == pg.K_c:
                self.__model.hold()
        elif event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                self.__model.stop_move_right()
            elif event.key == pg.K_LEFT:
                self.__model.stop_move_left()
            elif event.key == pg.K_DOWN:
                self.__model.stop_soft_drop()
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.__view.click()

    def run(self) -> None:
        # main loop for the game
        while True:
            # handles all current events
            for event in pg.event.get():
                self.handle(event)

            self.__model.update()

            self.__view.update()
