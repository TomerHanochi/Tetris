import pygame as pg

from tetris.assets.assets import Images
from tetris.view.view_object import ViewObject
from tetris.view.draw import Draw
from tetris.model.model import Model
from tetris.consts import Consts


class Board(ViewObject):
    def __init__(self, model: Model) -> None:
        self.__window = pg.display.get_surface()
        self.__model = model

    def draw_board_border(self, x: int, y: int) -> None:
        width, height = Consts.GRID_WIDTH + 2, Consts.GRID_HEIGHT + 2
        Draw.border(x, y, width, height)

    def draw_cur_tetromino(self, x: int, y: int) -> None:
        tetromino = self.model.cur_tetromino
        rotation = [(i, j) for (i, j) in tetromino.rotation if tetromino.y + j >= 0]
        Draw.tetromino(x + tetromino.x * Consts.BLOCK_SIZE, y + tetromino.y * Consts.BLOCK_SIZE,
                       rotation, tetromino.name)

    def draw_existing_blocks(self, x: int, y: int) -> None:
        for block in self.model.blocks:
            image = getattr(Images, block.parent)
            Draw.image(x + block.i * Consts.BLOCK_SIZE, y + block.j * Consts.BLOCK_SIZE, image)

    def draw(self) -> None:
        x = (Consts.SCREEN_WIDTH - Consts.GRID_WIDTH * Consts.BLOCK_SIZE) * .5
        y = (Consts.SCREEN_HEIGHT - (Consts.GRID_HEIGHT - 2) * Consts.BLOCK_SIZE) * .5

        self.draw_board_border(x - Consts.BLOCK_SIZE, y - Consts.BLOCK_SIZE)
        self.draw_cur_tetromino(x, y)
        self.draw_existing_blocks(x, y)

    @property
    def model(self) -> Model:
        return self.__model

    @property
    def window(self) -> pg.Surface:
        return self.__window
