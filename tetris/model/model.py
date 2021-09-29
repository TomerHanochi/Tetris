from tetris.consts import Consts
from tetris.model.board import Board
from tetris.model.tetromino import Tetromino
from tetris.model.tetromino_set import TetrominoSet
from tetris.model.ghost_tetromino import GhostTetromino
from tetris.ai.algorithm import Algorithm


class Model:
    """
    The main data structure for the game, includes:
    1. All Blocks
    2. Current tetromino
    3. Held tetromino
    4. Next Tetrominoes
    5. Ghost Tetrominoes
    """
    def __init__(self, use_cooldown: bool = True) -> None:
        self.__tetromino_set = TetrominoSet()
        self.__cur_tetromino = Tetromino(self.__tetromino_set.remove())
        self.__ghost_tetromino = GhostTetromino(x=self.cur_tetromino.x, y=self.cur_tetromino.y,
                                                rotation=self.cur_tetromino.rotation)
        self.__board = Board()
        # a property where the held tetromino can be stored
        self.__held_tetromino = None
        # a tetromino can be held only once per 'turn'
        self.__can_be_held = True

        # should: whether the command for the block to move was called
        # cooldown: the number of frames before a block moves
        self.__use_cooldown = use_cooldown
        self.__should_move_right = False
        self.__move_right_cooldown = 0
        self.__should_move_left = False
        self.__move_left_cooldown = 0
        self.__should_soft_drop = False
        self.__soft_drop_cooldown = 0
        self.__move_down_cooldown = 0

        # whether the game was paused
        self.__paused = False
        self.__pause_cooldown = 0

        self.__rows_cleared = 0
        self.__score = 0
        self.__high_score = int(open('tetris/model/highscore.txt', 'r').read())

    def update(self) -> None:
        if self.__pause_cooldown > 0:
            self.__pause_cooldown -= 1

        if self.terminal:
            self.set_high_score()
        elif not self.paused and self.pause_cooldown == 0:
            self.__ghost_tetromino.__init__(x=self.cur_tetromino.x, y=self.cur_tetromino.y,
                                            rotation=self.cur_tetromino.rotation)
            self.board.hard_drop(self.__ghost_tetromino)

            if self.__should_move_right and self.can_move_right:
                self.move_right()
            elif self.__move_right_cooldown > 0:
                self.__move_right_cooldown -= 1

            if self.__should_move_left and self.can_move_left:
                self.move_left()
            elif self.__move_left_cooldown > 0:
                self.__move_left_cooldown -= 1

            if self.__should_soft_drop and self.can_soft_drop:
                self.soft_drop()
            elif self.__soft_drop_cooldown > 0:
                self.__soft_drop_cooldown -= 1

            if self.__move_down_cooldown > 0:
                self.__move_down_cooldown -= 1

            # if there aren't enough tetrominoes in the set, generate new ones
            if len(self.__tetromino_set) <= Consts.NEXT_SET_SIZE:
                self.__tetromino_set.generate_new_tetrominoes()

            if self.can_move_down:
                Algorithm.do_move(cells=self.board.cells, cur_tetromino=self.cur_tetromino.name,
                                  next_tetromino=self.__tetromino_set.get_next()[0],
                                  held_tetromino=self.held_tetromino)
                self.move_down()
            # if the current tetromino can't move down, that means it needs to be replaced
            else:
                # the current tetrominoes blocks are appended to the all blocks list
                self.board.add_piece(self.cur_tetromino)

                cleared = self.board.clear_rows()
                if cleared:
                    self.__rows_cleared += cleared
                    # increase the score according to the row clear multiplier
                    self.__score += Consts.ROW_CLEAR_MULT[cleared - 1] * (self.level + 1)

                # replace tetromino
                self.__cur_tetromino.__init__(self.__tetromino_set.remove())
                # reset held 'cooldown'
                self.__can_be_held = True

    @property
    def can_move_right(self) -> bool:
        return ((not self.__use_cooldown or self.__move_right_cooldown == 0) and
                self.cur_tetromino.can_move_right(self.board.cells))

    def start_move_right(self) -> None:
        self.__should_move_right = True

    def move_right(self) -> None:
        self.cur_tetromino.move_right()
        self.__move_right_cooldown = Consts.HORIZONTAL_COOLDOWN

    def stop_move_right(self) -> None:
        self.__should_move_right = False

    @property
    def can_move_left(self) -> bool:
        return ((not self.__use_cooldown or self.__move_left_cooldown == 0) and
                self.cur_tetromino.can_move_left(self.board.cells))

    def start_move_left(self) -> None:
        self.__should_move_left = True

    def move_left(self) -> None:
        self.cur_tetromino.move_left()
        self.__move_left_cooldown = Consts.HORIZONTAL_COOLDOWN

    def stop_move_left(self) -> None:
        self.__should_move_left = False

    @property
    def can_move_down(self) -> bool:
        return self.cur_tetromino.can_move_down(self.board.cells)

    def move_down(self) -> None:
        if self.__move_down_cooldown == 0:
            self.cur_tetromino.move_down()
            self.__move_down_cooldown = Consts.COOLDOWN_BY_LEVEL[self.level]

    def rotate_right(self) -> None:
        self.cur_tetromino.rotate_right(self.board.cells)

    def rotate_left(self) -> None:
        self.cur_tetromino.rotate_left(self.board.cells)

    @property
    def can_soft_drop(self) -> bool:
        return ((not self.__use_cooldown or self.__soft_drop_cooldown == 0) and
                self.cur_tetromino.can_move_down(self.board.cells))

    def start_soft_drop(self) -> None:
        self.__should_soft_drop = True

    def soft_drop(self) -> None:
        self.cur_tetromino.move_down()
        self.__soft_drop_cooldown = Consts.SOFT_DROP_COOLDOWN
        # award points for each cell dropped in soft drop
        self.__score += Consts.SOFT_DROP_MULT

    def stop_soft_drop(self) -> None:
        self.__should_soft_drop = False

    def hard_drop(self) -> None:
        self.__score += self.board.hard_drop(self.cur_tetromino) * Consts.HARD_DROP_MULT

    def hold(self) -> None:
        if self.__can_be_held:
            if self.held_tetromino is None:
                # create a copy of the current tetromino
                self.__held_tetromino = self.cur_tetromino.name
                # switch the current one to a new one from the set
                self.__cur_tetromino.__init__(self.__tetromino_set.remove())
            else:
                # switch the held and current tetrominoes
                temp = self.__cur_tetromino.name
                self.__cur_tetromino.__init__(self.__held_tetromino)
                self.__held_tetromino = temp
            self.__can_be_held = False

    def set_high_score(self) -> None:
        if self.score > self.high_score:
            self.__high_score = self.score
            open('tetris/model/highscore.txt', 'w').write(str(self.score))

    def reset(self) -> None:
        self.set_high_score()
        self.__init__()

    def pause_or_resume(self) -> None:
        """Pauses or resumes the game"""
        self.__paused = not self.paused
        if not self.paused:
            # 3 extra seconds of pause
            self.__pause_cooldown = Consts.FRAME_RATE * 3

    @property
    def terminal(self) -> bool:
        """whether the game has ended"""
        return any(cell is not None for cell in self.board.cells[0])

    @property
    def next(self) -> list[str]:
        """get a list of the next Const.NEXT_SET_SIZE tetromino names"""
        return self.__tetromino_set.get_next()

    @property
    def cur_tetromino(self) -> Tetromino:
        return self.__cur_tetromino

    @property
    def ghost_tetromino(self) -> GhostTetromino:
        return self.__ghost_tetromino

    @property
    def held_tetromino(self) -> str:
        return self.__held_tetromino

    @property
    def board(self) -> Board:
        return self.__board

    @property
    def cleared(self) -> int:
        return self.__rows_cleared

    @property
    def score(self) -> int:
        return self.__score

    @property
    def high_score(self) -> int:
        return self.__high_score

    @property
    def level(self) -> int:
        # the level increases for every ten rows cleared and caps at 28
        level = int(self.cleared * .1)
        return level if level < 28 else 28

    @property
    def paused(self) -> bool:
        return self.__paused

    @property
    def pause_cooldown(self) -> int:
        return self.__pause_cooldown
