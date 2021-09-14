from tetris.assets.assets import Images
from tetris.view.utils.view_object import ViewObject
from tetris.view.utils.draw import Draw
from tetris.model.model import Model
from tetris.consts import Consts


class Board(ViewObject):
    def __init__(self, x: float, y: float, model: Model) -> None:
        self.__x = x
        self.__y = y
        self.__model = model

    def draw(self) -> None:
        Draw.border(self.x, self.y, self.w, self.h)

        # TODO Draw ghost tetromino

        # draws current tetromino
        tetromino = self.model.cur_tetromino
        Draw.tetromino(x=self.x + (tetromino.x + 1) * Consts.BLOCK_SIZE,
                       y=self.y + (tetromino.y + 1) * Consts.BLOCK_SIZE,
                       rotation=[(i, j) for (i, j) in tetromino.rotation if tetromino.y + j >= 0],
                       name=tetromino.name)

        # draws all existing blocks in board
        for block in self.model.blocks:
            Draw.image(x=self.x + (block.i + 1) * Consts.BLOCK_SIZE,
                       y=self.y + (block.j + 1) * Consts.BLOCK_SIZE,
                       image=getattr(Images, block.parent))

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def w(self) -> int:
        return Consts.GRID_WIDTH + 2

    @property
    def h(self) -> int:
        return Consts.GRID_HEIGHT + 2

    @property
    def model(self) -> Model:
        return self.__model
