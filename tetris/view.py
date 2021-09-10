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
        self.block_size = Consts.BLOCK_SIZE

    def draw_block(self, x: int, y: int, block) -> None:
        rect = (x + block.i * self.block_size, y + block.j * self.block_size, 0, 0)

        image = getattr(Images, block.parent)
        self.__window.blit(image, rect)

    def draw_border(self, x: int, y: int, width: int, height: int) -> None:
        image = getattr(Images, 'border')
        for i in range(width):
            pos_x, pos_y = x + i * self.block_size, y
            self.__window.blit(image, (pos_x, pos_y, 0, 0))
            self.__window.blit(image, (pos_x, pos_y + (height + 1) * self.block_size, 0, 0))
        for j in range(height):
            pos_x, pos_y = x, y + (j + 1) * self.block_size
            self.__window.blit(image, (pos_x, pos_y, 0, 0))
            self.__window.blit(image, (pos_x + (width - 1) * self.block_size, pos_y, 0, 0))

    def draw_tetromino(self, x, y, tetromino) -> None:
        for block in tetromino.blocks:
            if block.in_board:
                self.draw_block(x, y, block)

    def draw_board_border(self, x: int, y: int):
        width, height = Consts.GRID_WIDTH + 2, Consts.GRID_HEIGHT
        self.draw_border(x, y, width, height)

    def draw_next(self) -> None:
        width, height = 7, Consts.NEXT_SET_SIZE * 3 + 1
        x = self.block_size
        y = (self.__h - Consts.GRID_HEIGHT * self.block_size) * .5 + 3 * self.block_size
        self.draw_border(x, y, width, height)

        for j, tetromino in enumerate(self.__model.next):
            pos_x = x + (width - tetromino.width - 1) * self.block_size * .5 - \
                    tetromino.x * self.block_size
            pos_y = y + (j * 3 + 4) * self.block_size
            for block in tetromino.blocks:
                self.draw_block(pos_x, pos_y, block)

    def draw_held(self) -> None:
        width, height = 7, 4
        x = Consts.SCREEN_SIZE[0] - (width + 1) * self.block_size
        y = (self.__h - Consts.GRID_HEIGHT * self.block_size) * .5 + 3 * self.block_size
        self.draw_border(x, y, width, height)

        held = self.__model.held_tetromino
        if held is not None:
            pos_x = x + (width - held.width - 1) * self.block_size * .5 - held.x * self.block_size
            pos_y = y + (height - held.height + 1) * self.block_size * .5 + 2 * self.block_size
            for block in self.__model.held_tetromino.blocks:
                self.draw_block(pos_x, pos_y, block)

    def draw_current_tetromino(self, x: int, y: int):
        self.draw_tetromino(x, y, self.__model.cur_tetromino)

    def draw_ghost_tetromino(self, x: int, y: int) -> None:
        self.draw_tetromino(x, y, self.__model.ghost_tetromino)

    def draw_existing_blocks(self, x: int, y: int):
        for block in self.__model.blocks:
            if block.in_board:
                self.draw_block(x, y, block)

    def draw_board(self) -> None:
        block_size = Consts.BLOCK_SIZE
        x = (self.__w - Consts.GRID_WIDTH * block_size) * .5
        y = (self.__h - (Consts.GRID_HEIGHT - 2) * block_size) * .5

        self.draw_board_border(x - block_size, y - block_size)

        self.draw_ghost_tetromino(x, y)

        self.draw_current_tetromino(x, y)

        self.draw_existing_blocks(x, y)

    def update(self) -> None:
        self.__model.update(self.dt)

        self.__window.fill(Colors.background_color)

        self.draw_board()
        self.draw_next()
        self.draw_held()

        pg.display.flip()

        self.dt = self.__fps_clock.tick(self.__fps)
