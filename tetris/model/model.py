from tetris.consts import Consts
from tetris.model.block import Block
from tetris.model.tetromino import Tetromino
from tetris.model.tetromino_set import TetrominoSet
from tetris.model.ghost_tetromino import GhostTetromino


class Model:
    """
    The main data structure for the game, includes:
    1. All Blocks
    2. Current tetromino
    3. Held tetromino
    4. Next Tetrominoes
    5. Ghost Tetrominoes
    """
    def __init__(self) -> None:
        self.__tetromino_set = TetrominoSet()
        self.__cur_tetromino = self.__tetromino_set.remove()
        self.__ghost_tetromino = GhostTetromino(self.cur_tetromino, blocks=[])
        self.__blocks = []
        # a property where the held tetromino can be stored
        self.__held_tetromino = None
        # a tetromino can be held only once per 'turn'
        self.__can_be_held = True

        # should: whether the command for the block to move was called
        # cooldown: the number of frames before a block moves
        self.__should_move_right = False
        self.__move_right_cooldown = 0
        self.__should_move_left = False
        self.__move_left_cooldown = 0
        self.__should_soft_drop = False
        self.__soft_drop_cooldown = 0
        self.__move_down_cooldown = 0

        self.__rows_cleared = 0
        self.__score = 0

    def update(self) -> None:
        if not self.terminal:
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

            if self.can_move_down:
                self.move_down()
            # if the current tetromino can't move down, that means it needs to be replaced
            else:
                # the current tetrominoes blocks are appended to the all blocks list
                self.__blocks.extend(self.cur_tetromino.blocks)

                self.clear_rows()

                # if there aren't enough tetrominoes in the set, generate new ones
                if len(self.__tetromino_set) <= Consts.NEXT_SET_SIZE:
                    self.__tetromino_set.generate_new_tetrominoes()

                # replace tetromino
                self.__cur_tetromino = self.__tetromino_set.remove()
                # reset held 'cooldown'
                self.__can_be_held = True

    @property
    def can_move_right(self) -> bool:
        return self.cur_tetromino.can_move_right(self.blocks) and self.__move_right_cooldown == 0

    def start_move_right(self) -> None:
        self.__should_move_right = True

    def move_right(self) -> None:
        self.cur_tetromino.move_right()
        self.__move_right_cooldown = Consts.HORIZONTAL_COOLDOWN

    def stop_move_right(self) -> None:
        self.__should_move_right = False

    @property
    def can_move_left(self) -> bool:
        return self.cur_tetromino.can_move_left(self.blocks) and self.__move_left_cooldown == 0

    def start_move_left(self) -> None:
        self.__should_move_left = True

    def move_left(self) -> None:
        self.cur_tetromino.move_left()
        self.__move_left_cooldown = Consts.HORIZONTAL_COOLDOWN

    def stop_move_left(self) -> None:
        self.__should_move_left = False

    @property
    def can_move_down(self) -> bool:
        return self.cur_tetromino.can_move_down(self.blocks)

    def move_down(self) -> None:
        if self.__move_down_cooldown == 0:
            self.cur_tetromino.move_down()
            self.__move_down_cooldown = Consts.COOLDOWN_BY_LEVEL[self.level]

    def rotate_right(self) -> None:
        self.cur_tetromino.rotate_right()

    def rotate_left(self) -> None:
        self.cur_tetromino.rotate_left()

    @property
    def can_soft_drop(self) -> bool:
        return self.cur_tetromino.can_move_down(self.blocks) and self.__soft_drop_cooldown == 0

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
        while self.cur_tetromino.can_move_down(self.blocks):
            self.cur_tetromino.move_down()
            # award points for each cell dropped in hard drop
            self.__score += Consts.HARD_DROP_MULT

    def clear_rows(self) -> None:
        # list of indecies of the row of each block
        all_rows = [block.j for block in self.blocks]
        # a set of indecies of rows that are full
        clearable = {row for row in all_rows if all_rows.count(row) == Consts.GRID_WIDTH}
        if clearable:
            # a set of all blocks that are removable
            removable = {block for block in self.blocks if block.j in clearable}
            for block in removable:
                self.blocks.remove(block)
                del block

            # the lowest cleared row
            lowest_row_index = max(clearable)
            # indecies of rows above the lowest cleared row, sorted from the bottom to top
            floating_rows = sorted({block.j for block in self.blocks if block.j < lowest_row_index},
                                   reverse=True)
            # all floating blocks split by the rows they're in
            floating_blocks = [
                [block for block in self.blocks if block.j == floating_row_index]
                for floating_row_index in floating_rows
            ]
            for row in floating_blocks:
                # as long as none of the blocks in the current row can't move down, move down
                while all(not block.collide_down(other) for block in row for other in self.blocks
                          if other is not block) and all(block.can_move_down for block in row):
                    for block in row:
                        block.move_down()

        # the number of lines cleared (max of 4)
        cleared = len(clearable)
        # if there were cleared rows
        if cleared:
            self.__rows_cleared += cleared
            # increase the score according to the row clear multiplier
            self.__score += Consts.ROW_CLEAR_MULT[cleared - 1] * (self.level + 1)

    def hold(self) -> None:
        if self.__can_be_held:
            if self.held_tetromino is None:
                # create a copy of the current tetromino
                self.__held_tetromino = Tetromino(self.cur_tetromino.name)
                # switch the current one to a new one from the set
                self.__cur_tetromino = self.__tetromino_set.remove()
            else:
                # switch the held and current tetrominoes
                temp = self.__cur_tetromino
                self.__cur_tetromino = Tetromino(self.__held_tetromino.name)
                self.__held_tetromino = Tetromino(temp.name)
            self.__can_be_held = False

    def reset(self) -> None:
        self.__init__()

    @property
    def terminal(self) -> bool:
        # whether the game has ended
        return any(block.j <= 0 for block in self.blocks)

    @property
    def next(self) -> list[Tetromino]:
        # get a list of the next Const.NEXT_SET_SIZE next tetrominoes
        return self.__tetromino_set.get_next()

    @property
    def cur_tetromino(self) -> Tetromino:
        return self.__cur_tetromino

    @property
    def held_tetromino(self) -> Tetromino:
        return self.__held_tetromino

    @property
    def ghost_tetromino(self) -> GhostTetromino:
        self.__ghost_tetromino.update(self.cur_tetromino, self.blocks)
        return self.__ghost_tetromino

    @property
    def blocks(self) -> list[Block]:
        return self.__blocks

    @property
    def rows_cleared(self) -> int:
        return self.__rows_cleared

    @property
    def score(self) -> int:
        return self.__score

    @property
    def level(self) -> int:
        # the level increases for every ten rows cleared and caps at 28
        level = int(self.rows_cleared * .1)
        return level if level < 28 else 28
