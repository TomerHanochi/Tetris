from tetris.consts import Consts
from tetris.model.tetromino import Tetromino
from tetris.model.ghost_tetromino import GhostTetromino


class Board:
    def __init__(self) -> None:
        self.__cells = [[None for j in range(Consts.GRID_HEIGHT)] for i in range(Consts.GRID_WIDTH)]

    def add_piece(self, tetromino: Tetromino):
        for (i, j) in tetromino.rotation:
            self.__cells[tetromino.x + i][tetromino.y + j] = tetromino.name

    def hard_drop(self, tetromino: Tetromino or GhostTetromino) -> int:
        rows_dropped = 0
        while tetromino.can_move_down(self.cells):
            tetromino.move_down()
            rows_dropped += 1
        return rows_dropped

    @property
    def cells(self) -> list[list[str or None]]:
        return self.__cells
