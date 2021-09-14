from tetris.assets.assets import Fonts, Colors
from tetris.view.utils.view_object import ViewObject
from tetris.view.utils.draw import Draw
from tetris.model.model import Model
from tetris.consts import Consts


class Held(ViewObject):
    def __init__(self, x: float, y: float, model: Model) -> None:
        self.__x = (Consts.SCREEN_WIDTH + x - self.w * Consts.BLOCK_SIZE) * .5
        self.__y = y
        self.__model = model
        self.title = Fonts.sub_title.render('HELD', True, Colors.sub_title, Colors.background)

    def draw(self) -> None:
        Draw.border(self.x, self.y, self.w, self.h)

        Draw.image(x=self.x + (self.w * Consts.BLOCK_SIZE - self.title.get_width()) * .5,
                   y=self.y - self.title.get_height() * 1.25,
                   image=self.title)

        held = self.model.held_tetromino
        if held is not None:
            Draw.tetromino(x=self.x + (self.w - held.width) * Consts.BLOCK_SIZE * .5,
                           y=self.y + (self.h - held.height) * Consts.BLOCK_SIZE * .5,
                           rotation=held.rotation, name=held.name)

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def w(self) -> int:
        return 7

    @property
    def h(self) -> int:
        return 6

    @property
    def model(self) -> Model:
        return self.__model
