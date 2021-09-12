import pygame as pg

from tetris.utils.consts import Consts
from tetris.assets.assets import Colors, Images, Fonts
from tetris.model import Model

class View:
    def __init__(self, model: Model) -> None:
        self.__w, self.__h = Consts.SCREEN_SIZE
        self.__window = pg.display.set_mode(Consts.SCREEN_SIZE)
        self.__model = model
        self.__fps = Consts.FRAME_RATE
        self.__fps_clock = pg.time.Clock()

    def draw_title(self) -> None:
        block_size = Consts.BLOCK_SIZE
        title = Fonts.title.render('TETRIS', True, Colors.title, Colors.background)
        title_x = (self.__w - title.get_width()) * .5
        title_y = (self.__h - Consts.GRID_HEIGHT * block_size) * .5 - title.get_height() * 1.25
        self.__window.blit(title, (title_x, title_y))

    def draw_block(self, x: int, y: int, block) -> None:
        rect = (x + block.i * Consts.BLOCK_SIZE, y + block.j * Consts.BLOCK_SIZE)

        image = getattr(Images, block.parent)
        self.__window.blit(image, rect)

    def draw_border(self, x: int, y: int, width: int, height: int) -> None:
        image = getattr(Images, 'border')
        for i in range(width):
            pos_x, pos_y = x + i * Consts.BLOCK_SIZE, y
            self.__window.blit(image, (pos_x, pos_y))
            self.__window.blit(image, (pos_x, pos_y + (height + 1) * Consts.BLOCK_SIZE))
        for j in range(height):
            pos_x, pos_y = x, y + (j + 1) * Consts.BLOCK_SIZE
            self.__window.blit(image, (pos_x, pos_y))
            self.__window.blit(image, (pos_x + (width - 1) * Consts.BLOCK_SIZE, pos_y))

    def draw_tetromino(self, x, y, tetromino) -> None:
        for block in tetromino.blocks:
            if block.in_board:
                self.draw_block(x, y, block)

    def draw_board_border(self, x: int, y: int):
        width, height = Consts.GRID_WIDTH + 2, Consts.GRID_HEIGHT
        self.draw_border(x, y, width, height)

    def draw_next(self) -> None:
        width, height = 7, Consts.NEXT_SET_SIZE * 3 + 1
        x = Consts.BLOCK_SIZE
        y = (self.__h - (Consts.GRID_HEIGHT - 6) * Consts.BLOCK_SIZE) * .5
        self.draw_border(x, y, width, height)

        sub_title = Fonts.sub_title.render('NEXT', True, Colors.title, Colors.background)
        sub_title_x = x + (width * Consts.BLOCK_SIZE - sub_title.get_width()) * .5
        sub_title_y = y - sub_title.get_height() * 1.25
        self.__window.blit(sub_title, (sub_title_x, sub_title_y))

        for j, tetromino in enumerate(self.__model.next):
            pos_x = x + (width - tetromino.width - 1) * Consts.BLOCK_SIZE * .5 - \
                    tetromino.x * Consts.BLOCK_SIZE
            pos_y = y + (j * (tetromino.height + 2) + 4) * Consts.BLOCK_SIZE
            for block in tetromino.blocks:
                self.draw_block(pos_x, pos_y, block)

    def draw_held(self) -> None:
        width, height = 7, 4
        x = self.__w - (width + 1) * Consts.BLOCK_SIZE
        y = (self.__h - Consts.GRID_HEIGHT * Consts.BLOCK_SIZE) * .5 + 3 * Consts.BLOCK_SIZE
        self.draw_border(x, y, width, height)

        sub_title = Fonts.sub_title.render('HELD', True, Colors.title, Colors.background)
        sub_title_x = x + (width * Consts.BLOCK_SIZE - sub_title.get_width()) * .5
        sub_title_y = y - sub_title.get_height() * 1.25
        self.__window.blit(sub_title, (sub_title_x, sub_title_y))

        self.draw_statistics(x, y + (height + 2) * Consts.BLOCK_SIZE)

        held = self.__model.held_tetromino
        if held is not None:
            pos_x = x + (width - held.width - 1) * Consts.BLOCK_SIZE * .5 - held.x * Consts.BLOCK_SIZE
            pos_y = y + (height - held.height + 1) * Consts.BLOCK_SIZE * .5 + 2 * Consts.BLOCK_SIZE
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

    def draw_statistics(self, x: float, y: float) -> None:
        sub_title = Fonts.sub_title.render(f'SCORE', True, Colors.title,
                                           Colors.background)
        sub_title_y = y + sub_title.get_height() * 1.25
        self.__window.blit(sub_title, (x, sub_title_y))

        sub_title = Fonts.sub_title.render(f'{self.__model.score}', True, Colors.title,
                                           Colors.background)
        sub_title_y = sub_title_y + sub_title.get_height() * 1.25
        self.__window.blit(sub_title, (x, sub_title_y))

        sub_title = Fonts.sub_title.render(f'LEVEL', True, Colors.title,
                                           Colors.background)
        sub_title_y = sub_title_y + sub_title.get_height() * 1.25
        self.__window.blit(sub_title, (x, sub_title_y))

        sub_title = Fonts.sub_title.render(f'{self.__model.level}', True, Colors.title,
                                           Colors.background)
        sub_title_y = sub_title_y + sub_title.get_height() * 1.25
        self.__window.blit(sub_title, (x, sub_title_y))

        sub_title = Fonts.sub_title.render(f'CLEARED', True, Colors.title,
                                           Colors.background)
        sub_title_y = sub_title_y + sub_title.get_height() * 1.25
        self.__window.blit(sub_title, (x, sub_title_y))

        sub_title = Fonts.sub_title.render(f'{self.__model.rows_cleared}', True, Colors.title,
                                           Colors.background)
        sub_title_y = sub_title_y + sub_title.get_height() * 1.25
        self.__window.blit(sub_title, (x, sub_title_y))

    def update(self) -> None:
        self.__model.update()

        self.__window.fill(Colors.background)

        self.draw_title()
        self.draw_board()
        self.draw_next()
        self.draw_held()

        pg.display.flip()

        self.__fps_clock.tick(self.__fps)
