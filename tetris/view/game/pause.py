from tetris.view.assets import Fonts, Colors
from tetris.view.utils.view_object import ViewObject
from tetris.view.utils.context import Context
from tetris.model.model import Model
from tetris.consts import Consts


class Pause(ViewObject):
    def __init__(self, model: Model) -> None:
        self.__x = Consts.SCREEN_WIDTH * .5
        self.__y = Consts.SCREEN_HEIGHT * .5
        self.__model = model
        self.title = Fonts.title.render(f'PAUSE', True, Colors.title)

    def draw(self) -> None:
        if self.model.paused:
            Context.image(x=self.__x - self.title.get_width() * .5,
                       y=self.__y - self.title.get_height() * .5,
                       image=self.title)
        elif self.model.pause_cooldown != 0:
            image = Fonts.title.render(f'{self.model.pause_cooldown // Consts.FRAME_RATE + 1}',
                                       True, Colors.title)
            Context.image(x=self.__x - image.get_width() * .5, y=self.__y - image.get_height() * .5,
                       image=image)

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def model(self) -> Model:
        return self.__model
