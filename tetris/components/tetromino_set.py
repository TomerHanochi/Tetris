from random import shuffle

from tetris.components.tetromino import Tetromino

names = ['O']  # , 'I', 'J', 'L', 'Z', 'S', 'T']


class TetrominoSet:
    def __init__(self) -> None:
        self.__set = [Tetromino(name) for name in names]
        shuffle(self.__set)

    def remove(self) -> Tetromino:
        return self.__set.pop(0)
