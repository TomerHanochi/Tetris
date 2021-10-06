import pygame as pg

from tetris.view.assets import Colors, Sounds
from tetris.view.utils.clickable_view_object import ClickableViewObject
from tetris.view.utils.button import Button
from tetris.view.utils.key import Key
from tetris.view.game.board import Board
from tetris.view.game.held import Held
from tetris.view.game.next import Next
from tetris.view.game.statistics import Stats
from tetris.view.game.pause import Pause
from tetris.controller.controller import Controller
from tetris.consts import Consts


class View:
    def __init__(self) -> None:
        """ The class responsible for the gui of the game. """
        self.__w, self.__h = Consts.SCREEN_SIZE
        # the pygame display/window
        self.__window = pg.display.set_mode(Consts.SCREEN_SIZE)
        self.controller = Controller()
        # a clock to ensure the game runs at a constant fps
        self.__fps_clock = pg.time.Clock()
        # the stacking layers of the gui to choose what gets drawn over what
        self.__layers = []
        self.setup_game()
        # plays the tetris music on repeat
        Sounds.music.play(loops=-1)

    def click(self) -> None:
        for layer in reversed(self.__layers):
            for view_object in layer:
                if isinstance(view_object, ClickableViewObject) and view_object.is_clicked:
                    view_object.click()
                    return

    def setup_game(self) -> None:
        # Center part of the screen
        board = Board(x=(self.w - (Consts.GRID_WIDTH + 2) * Consts.BLOCK_SIZE) * .5,
                      y=(self.h - Consts.GRID_HEIGHT * Consts.BLOCK_SIZE) * .5)

        # Left part of the screen
        next_ = Next(x=board.x,
                     y=board.y + Consts.BLOCK_SIZE)

        reset_button = Button(x=next_.x,
                              y=next_.y + (next_.h + 1) * Consts.BLOCK_SIZE,
                              text='RESTART',
                              func=self.controller.reset_game)

        use_ai_button = Button(x=next_.x,
                               y=reset_button.y + reset_button.h + Consts.BLOCK_SIZE,
                               text='USE-AI',
                               func=self.controller.switch_use_ai)

        # Right part of the screen
        held = Held(x=board.x + board.w * Consts.BLOCK_SIZE,
                    y=board.y + Consts.BLOCK_SIZE)

        stats = Stats(x=board.x + board.w * Consts.BLOCK_SIZE,
                      y=held.y + held.h * Consts.BLOCK_SIZE)

        pause = Pause()

        self.__layers = [
            [next_, held, stats, board, reset_button, use_ai_button],
            [pause]
        ]

    def quit(self) -> None:
        self.controller.quit()
        pg.quit()
        exit()

    def process_input(self) -> None:
        """ Converts pygame events to controller calls. """
        for event in pg.event.get():
            # if the event is a key event, finds the key
            event_key = None
            if hasattr(event, 'key'):
                for key in Key:
                    if key.value == event.key:
                        event_key = key

            if event.type == pg.QUIT:
                self.quit()
            elif event_key is not None:
                if event.type == pg.KEYDOWN:
                    self.controller.key_down(event_key)
                elif event.type == pg.KEYUP:
                    self.controller.key_up(event_key)
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.click()

    def update(self) -> None:
        """Clears the screen, then redraws everything"""
        self.__window.fill(Colors.background)

        view_info = self.controller.view_info
        for layer in self.__layers:
            for view_object in layer:
                view_object.draw(view_info)

        pg.display.flip()

        # used to make sure the game runs at a constant fps
        self.__fps_clock.tick(Consts.FRAME_RATE)

    def run(self) -> None:
        """ Main loop for the game. """
        while True:
            self.process_input()

            self.controller.update()

            self.update()

    @property
    def w(self) -> int:
        return Consts.SCREEN_WIDTH

    @property
    def h(self) -> int:
        return Consts.SCREEN_HEIGHT
