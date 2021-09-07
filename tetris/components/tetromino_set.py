from random import shuffle

from tetris.components.tetromino import Tetromino

names = ['O', 'I', 'J', 'L', 'Z', 'S', 'T']


class TetrominoSet:
    def __init__(self) -> None:
        self.__set = [Tetromino(name) for name in names]
        shuffle(self.__set)

    def remove(self) -> Tetromino:
        return self.__set.pop(0)

    def generate_new_tetrominoes(self) -> None:
        new_set = [Tetromino(name) for name in names]
        shuffle(new_set)
        self.__set.extend(new_set)

    def __len__(self) -> int:
        return len(self.__set)
