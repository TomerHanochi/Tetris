from tetris.assets.assets import Fonts, Colors
from tetris.view.utils.view_object import ViewObject
from tetris.view.utils.draw import Draw
from tetris.model.model import Model
from tetris.consts import Consts


class Next(ViewObject):
    def __init__(self, x: float, y: float, model: Model) -> None:
        self.__x = (x - self.w * Consts.BLOCK_SIZE) * .5
        self.__y = y
        self.__model = model
        self.title = Fonts.sub_title.render('NEXT', True, Colors.sub_title, Colors.background)

    def draw(self) -> None:
        Draw.border(self.x, self.y, self.w, self.h)

        Draw.image(x=self.x + (self.w * Consts.BLOCK_SIZE - self.title.get_width()) * .5,
                   y=self.y - self.title.get_height() * 1.25,
                   image=self.title)

        for j, tetromino in enumerate(self.model.next):
            rotation = Consts.ROTATIONS[tetromino][0]
            xs = {x for (x, y) in rotation}
            # the width is the difference between the right and left blocks
            width = max(xs) - min(xs) + 1
            Draw.tetromino(x=self.x + (self.w - width) * Consts.BLOCK_SIZE * .5,
                           y=self.y + ((j + 1) * 3 - 1) * Consts.BLOCK_SIZE,
                           rotation=rotation, name=tetromino)

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
        return (Consts.NEXT_SET_SIZE + 1) * 3

    @property
    def model(self) -> Model:
        return self.__model
