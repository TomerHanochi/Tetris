from tetris.model.model import Model
from tetris.controller.view_info import ViewInfo
from tetris.view.utils.key import Key


class Controller:
    def __init__(self) -> None:
        """ Converts view processed events to the corresponding model functions. """
        self.__model = Model()

    def key_down(self, key) -> None:
        if key == Key.ESCAPE:
            self.__model.pause_or_resume()
        elif self.__model.playable:
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

    def key_up(self, key) -> None:
        if key == Key.RIGHT_ARROW:
            self.__model.stop_move_right()
        elif key == Key.LEFT_ARROW:
            self.__model.stop_move_left()
        elif key == Key.DOWN_ARROW:
            self.__model.stop_soft_drop()

    def switch_use_ai(self) -> None:
        self.__model.switch_use_ai()

    def update(self) -> None:
        self.__model.update()

    def reset(self) -> None:
        self.__model.reset()

    def quit(self) -> None:
        self.__model.set_high_score()

    @property
    def view_info(self) -> ViewInfo:
        return ViewInfo(self.__model)
