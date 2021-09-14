import pygame as pg

from tetris.assets.assets import Images
from tetris.model.model import Model
from tetris.view.view_object import ViewObject
from tetris.consts import Consts


class Board(ViewObject):
    def __init__(self, model: Model) -> None:
        self.__window = pg.display.get_surface()
        self.__model = model

    def draw_board_border(self, x: int, y: int) -> None:
        width, height = Consts.GRID_WIDTH + 2, Consts.GRID_HEIGHT + 2
        image = getattr(Images, 'border')
        for i in range(width):
            pos_x, pos_y = x + i * Consts.BLOCK_SIZE, y
            self.__window.blit(image, (pos_x, pos_y))
            self.__window.blit(image, (pos_x, pos_y + (height + 1) * Consts.BLOCK_SIZE))
        for j in range(height):
            pos_x, pos_y = x, y + j * Consts.BLOCK_SIZE
            self.__window.blit(image, (pos_x, pos_y))
            self.__window.blit(image, (pos_x + (width - 1) * Consts.BLOCK_SIZE, pos_y))

    def draw_tetromino(self, x: int, y: int) -> None:
        pass

    def draw(self) -> None:
        x = (Consts.SCREEN_WIDTH - Consts.GRID_WIDTH * Consts.BLOCK_SIZE) * .5
        y = (Consts.SCREEN_HEIGHT - (Consts.GRID_HEIGHT - 2) * Consts.BLOCK_SIZE) * .5

        self.draw_board_border(x - Consts.BLOCK_SIZE, y - Consts.BLOCK_SIZE)
        # self.draw_ghost_tetromino(x, y)
        # self.draw_current_tetromino(x, y)
        # self.draw_existing_blocks(x, y)

    @property
    def model(self) -> Model:
        return self.__model

    @property
    def window(self) -> pg.Surface:
        return self.__window
