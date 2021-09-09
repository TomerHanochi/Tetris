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

    def update(self, dt: int) -> None:
        if self.terminal:
            pass
        else:
            if self.cur_tetromino.can_move_down(self.blocks):
                self.cur_tetromino.move_down(.003 * dt)
            else:
                self.__blocks.extend(self.cur_tetromino.blocks)

                self.clear_rows()

                if len(self.__tetromino_set) <= Consts.NEXT_SET_SIZE:
                    self.__tetromino_set.generate_new_tetrominoes()

                self.__cur_tetromino = self.__tetromino_set.remove()
                self.__can_be_held = True

    def move_tetromino_right(self) -> None:
        if self.cur_tetromino.can_move_right(self.blocks):
            self.cur_tetromino.move_right()

    def move_tetromino_left(self) -> None:
        if self.cur_tetromino.can_move_left(self.blocks):
            self.cur_tetromino.move_left()

    def rotate_tetromino_right(self) -> None:
        self.cur_tetromino.rotate_right()

    def rotate_tetromino_left(self) -> None:
        self.cur_tetromino.rotate_left()

    def drop_tetromino(self) -> None:
        while self.cur_tetromino.can_move_down(self.blocks):
            self.cur_tetromino.move_down(1)

    def clear_rows(self) -> None:
        # TODO beautify this
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
                quit_loop = False
                while not quit_loop:
                    for block in row:
                        for other in self.blocks:
                            if other is not block and block.collide_down(other):
                                quit_loop = True
                                break
                        if not block.can_move_down:
                            quit_loop = True
                        if quit_loop:
                            break
                    if not quit_loop:
                        for block in row:
                            block.move_down(1)

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
