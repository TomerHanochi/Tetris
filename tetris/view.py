import pygame as pg

from tetris.utils.consts import Consts
from tetris.assets.assets import Colors, Images


class View:
    def __init__(self, model) -> None:
        self.__w, self.__h = Consts.SCREEN_SIZE
        self.__window = pg.display.set_mode(Consts.SCREEN_SIZE)
        self.__model = model
        self.dt = 0
        self.__fps = 60
        self.__fps_clock = pg.time.Clock()

    def draw_grid(self, x: int, y: int):
        self.__window.blit(Images.grid, (x, y, 0, 0))

    def draw_current_tetromino(self, x: int, y: int, block_size: int):
        current_tetromino = self.__model.cur_tetromino
        for block in current_tetromino.blocks:
            if block.in_board:
                rect = (x + block.i * block_size, y + block.j * block_size, 0, 0)
                image = getattr(Images, block.parent)
                self.__window.blit(image, rect)

    def draw_ghost_tetromino(self, x: int, y: int, block_size: int) -> None:
        ghost_tetromino = self.__model.ghost_tetromino
        for block in ghost_tetromino.blocks:
            rect = (x + block.i * block_size, y + block.j * block_size, 0, 0)
            image = getattr(Images, block.parent)
            self.__window.blit(image, rect)

    def draw_existing_blocks(self, x: int, y: int, block_size: int):
        for block in self.__model.blocks:
            if block.in_board:
                rect = (x + block.i * block_size, y + block.j * block_size, 0, 0)
                image = getattr(Images, block.parent)
                self.__window.blit(image, rect)

    def draw_board(self) -> None:
        block_size = Consts.BLOCK_SIZE
        x = (self.__w - Consts.GRID_WIDTH * block_size) / 2
        y = (self.__h - (Consts.GRID_HEIGHT - 2) * block_size) / 2

        self.draw_grid(x - block_size, y - block_size)

        self.draw_current_tetromino(x, y, block_size)

        self.draw_ghost_tetromino(x, y, block_size)

        self.draw_existing_blocks(x, y, block_size)

    def update(self) -> None:
        self.__model.update(self.dt)

        self.__window.fill(Colors.background_color)

        self.draw_board()

        pg.display.flip()

        self.dt = self.__fps_clock.tick(self.__fps)
