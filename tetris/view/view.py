import pygame as pg

from tetris.assets.assets import Colors, Fonts, Sounds
from tetris.view.utils.view_object import ViewObject
from tetris.view.utils.draw import Draw
from tetris.view.utils.button import Button
from tetris.view.game.board import Board
from tetris.view.game.held import Held
from tetris.view.game.next import Next
from tetris.view.game.statistics import Stats
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
        # the stacking layers of the gui to choose what gets printed over what
        self.__layers = [[], []]
        self.setup_game()
        Sounds.music.play(loops=-1)

    def draw_title(self) -> None:
        title = Fonts.title.render('TETRIS', True, Colors.title, Colors.background)
        title_x = (Consts.SCREEN_WIDTH - title.get_width()) * .5
        title_y = (Consts.SCREEN_HEIGHT - Consts.GRID_HEIGHT * Consts.BLOCK_SIZE) * .5 - title.get_height() * 1.25
        Draw.image(title_x, title_y, title)

    def click(self) -> None:
        for layer in reversed(self.layers):
            for view_object in layer:
                if isinstance(view_object, Button) and view_object.is_clicked:
                    view_object.click()

    def setup_game(self) -> None:
        # Center part of the screen
        board = Board(x=(self.w - (Consts.GRID_WIDTH + 2) * Consts.BLOCK_SIZE) * .5,
                      y=(self.h - Consts.GRID_HEIGHT * Consts.BLOCK_SIZE) * .5,
                      model=self.model)

        # Left part of the screen
        next_ = Next(x=board.x,
                     y=board.y + Consts.BLOCK_SIZE,
                     model=self.model)

        reset_button = Button(x=next_.x,
                              y=next_.y + (next_.h + 1) * Consts.BLOCK_SIZE,
                              text='RESTART', func=self.model.reset)

        # Right part of the screen
        held = Held(x=board.x + board.w * Consts.BLOCK_SIZE,
                    y=board.y + Consts.BLOCK_SIZE,
                    model=self.model)

        stats = Stats(x=board.x + board.w * Consts.BLOCK_SIZE,
                      y=held.y + held.h * Consts.BLOCK_SIZE,
                      model=self.model)

        self.layers[0].extend([next_, held, stats, board, reset_button])

    def update(self) -> None:
        """
        Clears the screen, then redraws everything
        """
        self.__window.fill(Colors.background)

        for layer in self.layers:
            for view_object in layer:
                view_object.draw()

        self.draw_title()

        pg.display.flip()

        # used to make sure the game runs at a stable fps
        self.__fps_clock.tick(self.__fps)

    @property
    def layers(self) -> list[list[ViewObject]]:
        return self.__layers

    @property
    def model(self) -> Model:
        return self.__model

    @property
    def w(self) -> int:
        return Consts.SCREEN_WIDTH

    @property
    def h(self) -> int:
        return Consts.SCREEN_HEIGHT
