import pygame as pg

from tetris.utils.consts import Consts
from tetris.assets.assets import Colors


class View:
    def __init__(self, controller) -> None:
        self.__w, self.__h = Consts.SCREEN_SIZE
        self.__window = pg.display.set_mode(Consts.SCREEN_SIZE)
        self.__controller = controller

    def draw_grid(self) -> None:
        block_size = Consts.BLOCK_SIZE
        x = (self.__w - Consts.GRID_WIDTH * block_size) / 2
        y = (self.__h - Consts.GRID_HEIGHT * block_size) / 2

        # draws the grid
        for i in range(Consts.GRID_WIDTH):
            for j in range(Consts.GRID_HEIGHT):
                rect = (x + i * block_size, y + j * block_size, block_size, block_size)
                pg.draw.rect(self.__window, Colors.grid_color, rect, 1)

        # draws current tetromino
        current_tetromino = self.__model.cur_tetromino
        for block in current_tetromino.blocks:
            if block.in_board:
                rect = (x + block.i * block_size, y + block.j * block_size, block_size, block_size)
                self.__window.fill(block.color, rect)

        # TODO draw tetromino hint highlight
        # draws the current tetromino location hint

        # draws all existing blocks in the grid
        for block in self.__model.blocks:
            if block.in_board:
                rect = (x + block.i * block_size, y + block.j * block_size, block_size, block_size)
                self.__window.fill(block.color, rect)

    def update(self) -> None:
        self.__window.fill(Colors.background_color)

        self.draw_grid()

        pg.display.flip()

    @property
    def __model(self):
        return self.__controller.model
