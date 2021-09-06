from tetris.components.tetromino_set import TetrominoSet
from tetris.components.tetromino import Tetromino


class Model:
    def __init__(self) -> None:
        self.cur_set = TetrominoSet()
        self.cur = self.cur_set.remove()
        self.blocks = []

    def update(self) -> None:
        self.cur_tetromino.move_down()

    @property
    def cur_tetromino(self) -> Tetromino:
        return self.cur
