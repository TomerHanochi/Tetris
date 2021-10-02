from random import shuffle

from tetris.consts import Consts


class TetrominoQueue:
    def __init__(self) -> None:
        """
        The set of tetrominoes used to generate new tetrominoes every time there aren't enough
        It works by taking all of the names in Consts.TETROMINO_NAMES and shuffling them,
        Then creates a tetromino for each. This ensures that you get each piece at least once within
        7 turns.
        """
        self.__queue = []
        self.generate_new_tetrominoes()

    def remove(self) -> str:
        """Returns the first tetromino in the set"""
        return self.__queue.pop(0)

    def generate_new_tetrominoes(self) -> None:
        """Adds 7 more tetrominoes according to algorithm mentioned in the __init__"""
        new_set = [name for name in Consts.TETROMINO_NAMES]
        shuffle(new_set)
        self.__queue.extend(new_set)

    def get_next(self) -> list[str]:
        """Returns the next Consts.NEXT_SET_SIZE tetrominoes"""
        return self.__queue[:Consts.NEXT_SET_SIZE]

    def __len__(self) -> int:
        return len(self.__queue)
