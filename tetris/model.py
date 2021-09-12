from tetris.utils.consts import Consts
from tetris.components.block import Block
from tetris.components.tetromino import Tetromino
from tetris.components.tetromino_set import TetrominoSet
from tetris.components.ghost_tetromino import GhostTetromino


class Model:
    def __init__(self) -> None:
        self.__tetromino_set = TetrominoSet()
        self.__cur_tetromino = self.__tetromino_set.remove()
        self.__blocks = []
        self.__ghost_tetromino = GhostTetromino(self.cur_tetromino, self.blocks)
        self.__held_tetromino = None
        self.__can_be_held = True
        self.__should_move_right = False
        self.__move_right_cooldown = 0
        self.__should_move_left = False
        self.__move_left_cooldown = 0
        self.__move_down_cooldown = 0
        self.__should_soft_drop = False
        self.__soft_drop_cooldown = 0
        self.__rows_cleared = 0
        self.__score = 0
        self.__cells_dropped = 0

    def update(self) -> None:
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
        else:
            self.__blocks.extend(self.cur_tetromino.blocks)

            self.clear_rows()

            if len(self.__tetromino_set) <= Consts.NEXT_SET_SIZE:
                self.__tetromino_set.generate_new_tetrominoes()

            self.__cur_tetromino = self.__tetromino_set.remove()
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
        self.__score += Consts.SOFT_DROP_MULT

    def stop_soft_drop(self) -> None:
        self.__should_soft_drop = False

    def hard_drop(self) -> None:
        while self.cur_tetromino.can_move_down(self.blocks):
            self.cur_tetromino.move_down()
            self.__score += Consts.HARD_DROP_MULT

    def clear_rows(self) -> None:
        indecies = [block.j for block in self.blocks]
        indecies = {index for index in indecies if indecies.count(index) == Consts.GRID_WIDTH}
        clearable = {block for block in self.blocks if block.j in indecies}
        for block in clearable:
            self.blocks.remove(block)
            del block

        if indecies:
            lowest_row_index = max(indecies)
            rows = sorted({block.j for block in self.blocks if block.j < lowest_row_index},
                          reverse=True)
            floating = [
                [block for block in self.blocks if block.j == row] for row in rows
            ]
            for row in floating:
                while all(not block.collide_down(other) for block in row for other in self.blocks
                          if other is not block) and all(block.can_move_down for block in row):
                    for block in row:
                        block.move_down()

        cleared = len(indecies)
        if cleared:
            self.__rows_cleared += cleared
            self.__score += Consts.ROW_CLEAR_MULT[cleared - 1] * (self.level + 1)

    def hold(self) -> None:
        if self.__can_be_held:
            if self.held_tetromino is None:
                self.__held_tetromino = Tetromino(self.cur_tetromino.name)
                self.__cur_tetromino = self.__tetromino_set.remove()
            else:
                temp = self.__cur_tetromino
                self.__cur_tetromino = Tetromino(self.__held_tetromino.name)
                self.__held_tetromino = Tetromino(temp.name)
            self.__can_be_held = False

    @property
    def terminal(self) -> bool:
        return any(block.j <= 0 for block in self.blocks)

    @property
    def next(self) -> list[Tetromino]:
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
    def level(self) -> int:
        level = int(self.rows_cleared * .1)
        return (0 if level < 0 else
                level if level < 28 else 28)

    @property
    def score(self) -> int:
        return self.__score
