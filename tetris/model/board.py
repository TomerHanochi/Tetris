from tetris.consts import Consts
from tetris.model.tetromino import Tetromino
from tetris.model.ghost_tetromino import GhostTetromino


class Board:
    def __init__(self) -> None:
        self.__cells = [[None for _ in range(Consts.GRID_WIDTH)] for _ in range(Consts.GRID_HEIGHT)]

    def add_piece(self, tetromino: Tetromino):
        for (i, j) in tetromino.rotation:
            self.__cells[tetromino.y + j][tetromino.x + i] = tetromino.name

    def clear_row(self, j) -> None:
        self.cells[j] = [None for _ in range(Consts.GRID_WIDTH)]

    def clear_rows(self) -> int:
        clearable = {j for j, row in enumerate(self.cells) if all(cell is not None for cell in row)}
        if clearable:
            for j in clearable:
                self.clear_row(j)

            # row above the last row to be cleared
            last_row = max(clearable) - 1
            # first row that has blocks in it
            first_row = 0
            for j, row in enumerate(self.cells):
                if any(cell is not None for cell in row):
                    first_row = j
                    break
            # all rows between them are floating
            for row in range(last_row, first_row - 1, -1):
                for cur in range(row, Consts.GRID_HEIGHT - 1):
                    if all(cell is None for cell in self.cells[cur + 1]):
                        self.cells[cur + 1] = self.cells[cur].copy()
                        self.cells[cur] = [None for _ in range(Consts.GRID_WIDTH)]
                    else:
                        break
        return len(clearable)

    def hard_drop(self, tetromino: Tetromino or GhostTetromino) -> int:
        rows_dropped = 0
        while tetromino.can_move_down(self.cells):
            tetromino.move_down()
            rows_dropped += 1
        return rows_dropped

    @property
    def cells(self) -> list[list[str or None]]:
        return self.__cells
