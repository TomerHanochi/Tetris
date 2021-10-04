from tetris.model.model import Model
from tetris.view.view import View
from tetris.view.events.event_handler import EventHandler
from tetris.view.events.event_type import EventType
from tetris.view.events.key import Key


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
            if key == Key.RIGHT_ARROW:
                self.__model.start_move_right()
            elif key == Key.LEFT_ARROW:
                self.__model.start_move_left()
            elif key == Key.UP_ARROW or key == Key.X:
                self.__model.rotate_right()
            elif key == Key.CONTROL or key == Key.Z:
                self.__model.rotate_left()
            elif key == Key.DOWN_ARROW:
                self.__model.start_soft_drop()
            elif key == Key.SPACE_BAR:
                self.__model.hard_drop()
            elif key == Key.SHIFT or key == Key.C:
                self.__model.hold()
        if key == Key.ESCAPE:
            self.__model.pause_or_resume()

    def player_key_up(self, key) -> None:
        if key == Key.RIGHT_ARROW:
            self.__model.stop_move_right()
        elif key == Key.LEFT_ARROW:
            self.__model.stop_move_left()
        elif key == Key.DOWN_ARROW:
            self.__model.stop_soft_drop()

    def handle(self, event) -> None:
        """Handles the various pygame events"""
        if event.type == EventType.QUIT:
            # if the close window button was clicked
            # update the high score and quit
            self.__model.set_high_score()
            self.__view.quit()
            exit()
        elif event.type == EventType.KEY_DOWN:
            self.player_key_down(event.key)
        elif event.type == EventType.KEY_UP:
            self.player_key_up(event.key)
        elif event.type == EventType.MOUSE_CLICKED:
            self.__view.click()

    def run(self) -> None:
        # main loop for the game
        while True:
            # handles all current events
            for event in EventHandler.get_events():
                self.handle(event)

            self.__model.update()

            self.__view.update()
