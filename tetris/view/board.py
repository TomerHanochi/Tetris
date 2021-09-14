import pygame as pg

from tetris.assets.assets import Images
from tetris.model.model import Model
from tetris.consts import Consts


class Board:
    def __init__(self, model: Model) -> None:
        self.__window = pg.display.get_surface()
        self.__model = model

    def draw_board_border(self, x: int, y: int) -> None:
        width, height = Consts.GRID_WIDTH, Consts.GRID_HEIGHT
        image = getattr(Images, 'border')
        pass

    def draw(self) -> None:
        x = (Consts.SCREEN_WIDTH - Consts.GRID_WIDTH * Consts.BLOCK_SIZE) * .5
        y = (Consts.SCREEN_HEIGHT - (Consts.GRID_HEIGHT - 2) * Consts.BLOCK_SIZE) * .5

        self.draw_board_border(x - Consts.BLOCK_SIZE, y - Consts.BLOCK_SIZE)
        self.draw_ghost_tetromino(x, y)
        self.draw_current_tetromino(x, y)
        self.draw_existing_blocks(x, y)

    @property
    def model(self) -> Model:
        return self.__model

    @property
    def window(self) -> pg.Surface:
        return self.__window
