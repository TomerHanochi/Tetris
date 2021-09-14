import pygame as pg

from tetris.assets.assets import Colors, Images, Fonts, Sounds
from tetris.view.view_object import ViewObject
from tetris.view.button import Button
from tetris.view.board import Board
from tetris.model.model import Model
from tetris.consts import Consts


class View:
    """
    The class responsible for the gui of the game
    """
    def __init__(self, model: Model) -> None:
        self.__w, self.__h = Consts.SCREEN_SIZE
        # the pygame display/window
        self.__window = pg.display.set_mode(Consts.SCREEN_SIZE)
        self.__model = model
        # the max fps the game can run in
        self.__fps = Consts.FRAME_RATE
        # a clock to ensure the game runs at that constant fps
        self.__fps_clock = pg.time.Clock()
        y = (self.__h - (Consts.GRID_HEIGHT - 16 - Consts.NEXT_SET_SIZE * 6) * Consts.BLOCK_SIZE) * .5
        self.__reset_button = Button(Consts.BLOCK_SIZE, y, 'RESTART', self.model.reset)
        # the stacking layers of the gui to choose what gets printed over what
        self.__layers = [[], []]
        self.setup_game()
        Sounds.music.play(loops=-1)

    def draw_title(self) -> None:
        title = Fonts.title.render('TETRIS', True, Colors.title, Colors.background)
        title_x = (self.__w - title.get_width()) * .5
        title_y = (self.__h - Consts.GRID_HEIGHT * Consts.BLOCK_SIZE) * .5 - title.get_height() * 1.25
        self.__window.blit(title, (title_x, title_y))

    def draw_block(self, x: int, y: int, block) -> None:
        rect = (x + block.i * Consts.BLOCK_SIZE, y + block.j * Consts.BLOCK_SIZE)

        image = getattr(Images, block.parent)
        self.__window.blit(image, rect)

    def draw_border(self, x: int, y: int, width: int, height: int) -> None:
        """
        Draws a border made of black blocks - assets/images/Border.png
        :param x: top left x
        :param y: top left y
        :param width: amount of blocks in width
        :param height: amount of blocks i  height - 2
        """
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
        """
        Draws the next Consts.NEXT_SET_SIZE tetrominoes,
        the border around them and the sub title
        """
        width, height = 7, Consts.NEXT_SET_SIZE * 3 + 1
        x = Consts.BLOCK_SIZE
        y = (self.__h - (Consts.GRID_HEIGHT - 2) * Consts.BLOCK_SIZE) * .5
        self.draw_border(x, y, width, height)

        sub_title = Fonts.sub_title.render('NEXT', True, Colors.sub_title, Colors.background)
        sub_title_x = x + (width * Consts.BLOCK_SIZE - sub_title.get_width()) * .5
        sub_title_y = y - sub_title.get_height() * 1.25
        self.__window.blit(sub_title, (sub_title_x, sub_title_y))

        for j, tetromino in enumerate(self.model.next):
            pos_x = x + (width - tetromino.width - 1) * Consts.BLOCK_SIZE * .5 - \
                    tetromino.x * Consts.BLOCK_SIZE
            pos_y = y + (j * 3 - Consts.Y_OFFSET + 2) * Consts.BLOCK_SIZE
            for block in tetromino.blocks:
                self.draw_block(pos_x, pos_y, block)

    def draw_statistics(self, x: float, y: float) -> None:
        """Draws the statistics, at an even distance from each other"""
        statistics = [('SCORE', f'{self.model.score}'),
                      ('LEVEL', f'{self.model.level}'),
                      ('CLEARED', f'{self.model.rows_cleared}'), ]
        sub_title_y = y
        for (title, value) in statistics:
            sub_title = Fonts.sub_title.render(title, True, Colors.statistic,
                                               Colors.background)
            sub_title_y += sub_title.get_height() * 2
            self.__window.blit(sub_title, (x, sub_title_y))

            sub_title = Fonts.sub_title.render(value, True, Colors.statistic,
                                               Colors.background)
            sub_title_y += sub_title.get_height() * 1.25
            self.__window.blit(sub_title, (x, sub_title_y))

    def draw_held(self) -> None:
        """
        Draws the held tetromino, the border around it, the sub title
        and the statistics right under it
        """
        width, height = 7, 4
        x = self.__w - (width + 1) * Consts.BLOCK_SIZE
        y = (self.__h - (Consts.GRID_HEIGHT - 2) * Consts.BLOCK_SIZE) * .5
        self.draw_border(x, y, width, height)

        sub_title = Fonts.sub_title.render('HELD', True, Colors.sub_title, Colors.background)
        sub_title_x = x + (width * Consts.BLOCK_SIZE - sub_title.get_width()) * .5
        sub_title_y = y - sub_title.get_height() * 1.25
        self.__window.blit(sub_title, (sub_title_x, sub_title_y))

        self.draw_statistics(x, y + (height + 2) * Consts.BLOCK_SIZE)

        held = self.model.held_tetromino
        if held is not None:
            pos_x = x + (width - held.width - 1 - held.x * 2) * Consts.BLOCK_SIZE * .5
            pos_y = y + (height - held.height - Consts.Y_OFFSET * 2 + 1) * Consts.BLOCK_SIZE * .5
            for block in self.model.held_tetromino.blocks:
                self.draw_block(pos_x, pos_y, block)

    def draw_current_tetromino(self, x: int, y: int):
        self.draw_tetromino(x, y, self.model.cur_tetromino)

    def draw_ghost_tetromino(self, x: int, y: int) -> None:
        self.draw_tetromino(x, y, self.model.ghost_tetromino)

    def draw_existing_blocks(self, x: int, y: int):
        for block in self.model.blocks:
            if block.in_board:
                self.draw_block(x, y, block)

    def draw_board(self) -> None:
        """Draws the entire board"""
        x = (self.__w - Consts.GRID_WIDTH * Consts.BLOCK_SIZE) * .5
        y = (self.__h - (Consts.GRID_HEIGHT - 2) * Consts.BLOCK_SIZE) * .5

        self.draw_board_border(x - Consts.BLOCK_SIZE, y - Consts.BLOCK_SIZE)
        self.draw_ghost_tetromino(x, y)
        self.draw_current_tetromino(x, y)
        self.draw_existing_blocks(x, y)

    def click(self) -> None:
        if self.__reset_button.is_clicked:
            self.__reset_button.click()

    def setup_game(self) -> None:
        self.layers[0].extend([
            Board(self.model)
        ])

    def update(self) -> None:
        """
        Clears the screen, then redraws everything
        """
        self.__window.fill(Colors.background)

        for layer in self.layers:
            for view_object in layer:
                view_object.draw()

        # self.draw_title()
        self.draw_board()
        # self.draw_next()
        # self.draw_held()
        # self.__reset_button.draw(self.__window)

        pg.display.flip()

        # used to make sure the game runs at a stable fps
        self.__fps_clock.tick(self.__fps)

    @property
    def layers(self) -> list[list[ViewObject]]:
        return self.__layers

    @property
    def model(self) -> Model:
        return self.__model
