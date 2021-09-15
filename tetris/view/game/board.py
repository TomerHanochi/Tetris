from tetris.assets.assets import Images, Fonts, Colors
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
        title = Fonts.title.render('TETRIS', True, Colors.title, Colors.background)
        Draw.image(x=self.x,
                   y=self.y - title.get_height() * 1.25,
                   image=title)

        Draw.border(self.x, self.y, self.w, self.h)

        tetromino = self.model.ghost_tetromino
        Draw.tetromino(x=self.x + (tetromino.x + 1) * Consts.BLOCK_SIZE,
                       y=self.y + (tetromino.y + 1) * Consts.BLOCK_SIZE,
                       rotation=tetromino.rotation, name='ghost')

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
