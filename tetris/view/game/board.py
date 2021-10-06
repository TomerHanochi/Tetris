from tetris.controller.view_info import ViewInfo
from tetris.view.assets import Images, Fonts, Colors
from tetris.view.utils.view_object import ViewObject
from tetris.view.utils.context import Context
from tetris.consts import Consts


class Board(ViewObject):
    def __init__(self, x: float, y: float) -> None:
        self.__x = x
        self.__y = y
        self.title = Fonts.title.render('TETRIS', True, Colors.title)

    def draw(self, view_info: ViewInfo) -> None:
        # Draws the pre rendered tetris title
        Context.image(x=self.x,
                      y=self.y - self.title.get_height() * 1.25,
                      image=self.title)

        Context.border(self.x, self.y, self.w, self.h)

        # draws the ghost tetromino
        Context.tetromino(x=self.x + (view_info.ghost_tetromino_x + 1) * Consts.BLOCK_SIZE,
                          y=self.y + (view_info.ghost_tetromino_y + 1) * Consts.BLOCK_SIZE,
                          rotation=view_info.ghost_tetromino_rotation, name='ghost')

        # draws current tetromino
        Context.tetromino(x=self.x + (view_info.cur_tetromino_x + 1) * Consts.BLOCK_SIZE,
                          y=self.y + (view_info.cur_tetromino_y + 1) * Consts.BLOCK_SIZE,
                          rotation=view_info.cur_tetromino_rotation,
                          name=view_info.cur_tetromino)

        # draws all existing blocks in board
        for (i, j, name) in view_info.blocks:
            Context.image(x=self.x + (i + 1) * Consts.BLOCK_SIZE,
                          y=self.y + (j + 1) * Consts.BLOCK_SIZE,
                          image=getattr(Images, name))

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
