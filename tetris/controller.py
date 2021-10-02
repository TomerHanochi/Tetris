import pygame as pg

from tetris.model.model import Model
from tetris.view.view import View
from tetris.ai.events import Events


class Controller:
    def __init__(self) -> None:
        """
        Handles all user input and the main loop of the game
        Controls both the view and the model
        """
        self.__model = Model()
        self.__view = View(self.__model)

    def player_key_down(self, key) -> None:
        if not self.__model.paused and self.__model.pause_cooldown == 0 and \
                not self.__model.terminal:
            if key == pg.K_RIGHT:
                self.__model.start_move_right()
            elif key == pg.K_LEFT:
                self.__model.start_move_left()
            elif key == pg.K_UP or key == pg.K_x:
                self.__model.rotate_right()
            elif key == pg.KMOD_CTRL or key == pg.K_z:
                self.__model.rotate_left()
            elif key == pg.K_DOWN:
                self.__model.start_soft_drop()
            elif key == pg.K_SPACE:
                self.__model.hard_drop()
            elif key == pg.KMOD_SHIFT or key == pg.K_c:
                self.__model.hold()
        if key == pg.K_ESCAPE:
            self.__model.pause_or_resume()

    def player_key_up(self, key) -> None:
        if key == pg.K_RIGHT:
            self.__model.stop_move_right()
        elif key == pg.K_LEFT:
            self.__model.stop_move_left()
        elif key == pg.K_DOWN:
            self.__model.stop_soft_drop()

    def ai_key_down(self, key) -> None:
        if not self.__model.paused and self.__model.pause_cooldown == 0:
            if key == pg.K_RIGHT and self.__model.can_move_right:
                self.__model.move_right()
            elif key == pg.K_LEFT and self.__model.can_move_left:
                self.__model.move_left()
            elif key == pg.K_x:
                self.__model.rotate_right()
            elif key == pg.K_SPACE:
                self.__model.hard_drop()
            elif key == pg.K_c:
                self.__model.hold()

    def handle(self, event) -> None:
        """Handles the various pygame events"""
        if event.type == pg.QUIT:
            # if the close window button was clicked
            # update the high score and quit
            self.__model.set_high_score()
            pg.quit()
            exit()
        elif event.type == pg.KEYDOWN:
            self.player_key_down(event.key)
        elif event.type == pg.KEYUP:
            self.player_key_up(event.key)
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.__view.click()
        elif event.type == Events.AI_MOVE:
            self.ai_key_down(event.key)

    def run(self) -> None:
        # main loop for the game
        while True:

            # handles all current events
            for event in pg.event.get():
                self.handle(event)

            self.__model.update()

            self.__view.update()
