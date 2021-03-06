from tetris.controller.view_info import ViewInfo
from tetris.view.assets import Fonts, Colors
from tetris.view.utils.view_object import ViewObject
from tetris.view.utils.context import Context
from tetris.consts import Consts


class Next(ViewObject):
    def __init__(self, x: float, y: float) -> None:
        self.__x = (x - self.w * Consts.BLOCK_SIZE) * .5
        self.__y = y
        self.title = Fonts.sub_title.render('NEXT', True, Colors.sub_title)

    def draw(self, view_info: ViewInfo) -> None:
        Context.border(self.x, self.y, self.w, self.h)

        # Draws the pre rendered next title
        Context.image(x=self.x + (self.w * Consts.BLOCK_SIZE - self.title.get_width()) * .5,
                      y=self.y - self.title.get_height() * 1.25,
                      image=self.title)

        # for each held tetromino, draw it
        for j, tetromino in enumerate(view_info.next_tetrominoes):
            rotation = Consts.ROTATIONS[tetromino][0]
            xs = {x for (x, y) in rotation}
            # the width is the difference between the right and left blocks
            width = max(xs) - min(xs) + 1
            Context.tetromino(x=self.x + (self.w - width) * Consts.BLOCK_SIZE * .5,
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
