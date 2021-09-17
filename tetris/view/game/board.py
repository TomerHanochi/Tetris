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
        self.title = Fonts.title.render('TETRIS', True, Colors.title)

    def draw(self) -> None:
        # Draws the pre rendered tetris title
        Draw.image(x=self.x,
                   y=self.y - self.title.get_height() * 1.25,
                   image=self.title)

        Draw.border(self.x, self.y, self.w, self.h)

        # draws the ghost tetromino
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
        blocks = [(i, j, self.model.board.cells[j][i])
                  for i in range(Consts.GRID_WIDTH) for j in range(Consts.GRID_HEIGHT)
                  if self.model.board.cells[j][i] is not None]
        for (i, j, parent) in blocks:
            Draw.image(x=self.x + (i + 1) * Consts.BLOCK_SIZE,
                       y=self.y + (j + 1) * Consts.BLOCK_SIZE,
                       image=getattr(Images, parent))

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
