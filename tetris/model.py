from tetris.utils.consts import Consts
from tetris.components.block import Block
from tetris.components.tetromino import Tetromino
from tetris.components.tetromino_set import TetrominoSet


class Model:
    def __init__(self) -> None:
        self.__tetromino_set = TetrominoSet()
        self.__cur = self.__tetromino_set.remove()
        self.__blocks = []

    def update(self, dt) -> None:
        if self.terminal:
            pass
        else:
            if self.cur_tetromino.can_move_down(self.blocks):
                self.cur_tetromino.move_down(.003 * dt)
            else:
                self.__blocks.extend(self.cur_tetromino.blocks)

                if len(self.__tetromino_set) <= Consts.NEXT_SET_SIZE:
                    self.__tetromino_set.generate_new_tetrominoes()

                self.__cur = self.__tetromino_set.remove()

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

    @property
    def terminal(self) -> bool:
        return any(block.j <= 0 for block in self.blocks)

    @property
    def cur_tetromino(self) -> Tetromino:
        return self.__cur

    @property
    def blocks(self) -> list[Block]:
        return self.__blocks
