from __future__ import annotations

from tetris.consts import Consts
from tetris.model.tetromino import Tetromino
from tetris.model.ghost_tetromino import GhostTetromino


class Board:
    def __init__(self, cells: list[list[str | None]] = None) -> None:
        """
        A class representing a tetris board.
        :param cells: a matrix representing the board state
        """
        if cells is None:
            self.__cells = [[None for _ in range(Consts.GRID_WIDTH)]
                            for _ in range(Consts.GRID_HEIGHT)]
        else:
            self.__cells = [[cell for cell in row] for row in cells]

    def add_piece(self, tetromino: Tetromino):
        """ Adds the blocks of a tetromino to the board """
        for (i, j) in tetromino.rotation:
            if tetromino.y + j >= 0:
                # the name is used so it is possible to get the tile image later
                self.__cells[tetromino.y + j][tetromino.x + i] = tetromino.name

    def clear_row(self, j) -> None:
        """
        Replaces a row with an empty row
        :param j: the index of the row to clear
        """
        self.cells[j] = [None for _ in range(Consts.GRID_WIDTH)]

    def clear_rows(self) -> int:
        """
        Clears all filled rows
        :return: number of rows cleared
        """
        # the rows that are full
        clearable = {j for j, row in enumerate(self.cells) if all(cell is not None for cell in row)}
        # if clearable isn't empty
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
            # move each row down until it can't
            for row in range(last_row, first_row - 1, -1):
                for cur in range(row, Consts.GRID_HEIGHT - 1):
                    # as long as the row below is empty, move down
                    if all(cell is None for cell in self.cells[cur + 1]):
                        self.cells[cur + 1] = self.cells[cur].copy()
                        self.clear_row(cur)
                    else:
                        break
        return len(clearable)

    def hard_drop(self, tetromino: Tetromino | GhostTetromino) -> int:
        """
        Hard drops a tetromino
        :param tetromino: a tetromino to hard drop
        :return: number of rows dropped
        """
        rows_dropped = 0
        while tetromino.can_move_down(self.cells):
            tetromino.move_down()
            rows_dropped += 1
        return rows_dropped

    @property
    def cells(self) -> list[list[str | None]]:
        return self.__cells

    @cells.setter
    def cells(self, cells: list[list[str | None]]) -> None:
        if len(cells) == Consts.GRID_HEIGHT and len(cells[0]) == Consts.GRID_WIDTH:
            self.__cells = [[cell for cell in row] for row in cells]
        else:
            raise ValueError(
                f'Size doesn\'t match. expected {Consts.GRID_HEIGHT}x{Consts.GRID_WIDTH} ' +
                f'got {len(cells)}x{len(cells[0])}'
            )
