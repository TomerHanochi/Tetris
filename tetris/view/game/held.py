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
            rotation = Consts.ROTATIONS[held][0]
            xs, ys = set(), set()
            for (x, y) in rotation:
                xs.add(x)
                ys.add(y)
            # the width is the difference between the right and left blocks
            width = max(xs) - min(xs) + 1
            # the height is the difference between the bottom and top blocks
            height = max(ys) - min(ys) + 1
            Draw.tetromino(x=self.x + (self.w - width) * Consts.BLOCK_SIZE * .5,
                           y=self.y + (self.h - height) * Consts.BLOCK_SIZE * .5,
                           rotation=rotation, name=held)

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
