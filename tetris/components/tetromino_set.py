from random import shuffle

from tetris.components.tetromino import Tetromino
from tetris.utils.consts import Consts


class TetrominoSet:
    def __init__(self) -> None:
        """
        The set of tetrominoes used to generate new tetrominoes every time there aren't enough
        It works by taking all of the names in Consts.TETROMINO_NAMES and shuffling them,
        Then creates a tetromino for each. This ensures that you get each piece at least once within
        7 turns.
        """
        self.__set = []
        self.generate_new_tetrominoes()

    def remove(self) -> Tetromino:
        """Returns the first tetromino in the set"""
        return self.__set.pop(0)

    def generate_new_tetrominoes(self) -> None:
        """Adds 7 more tetrominoes according to algorithm mentioned in the __init__"""
        new_set = [Tetromino(name) for name in Consts.TETROMINO_NAMES]
        shuffle(new_set)
        self.__set.extend(new_set)

    def get_next(self) -> list[Tetromino]:
        """Returns the next Consts.NEXT_SET_SIZE tetrominoes"""
        return self.__set[:Consts.NEXT_SET_SIZE]

    def __len__(self) -> int:
        return len(self.__set)
