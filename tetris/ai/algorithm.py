from tetris.consts import Consts
from tetris.ai.network import Network
from tetris.ai.events import Events
from tetris.model.board import Board
from tetris.model.tetromino import Tetromino

from random import uniform


class Move:
    def __init__(self, right: int = 0, left: int = 0, rotate: int = 0) -> None:
        self.__right = right
        self.__left = left
        self.__rotate = rotate

    @property
    def right(self) -> int:
        return self.__right

    @property
    def left(self) -> int:
        return self.__left

    @property
    def turn(self) -> int:
        return self.__rotate

    def __str__(self) -> str:
        return f'{self.turn=}, {self.right=}, {self.left=}'


class Algorithm:
    @staticmethod
    def get_rotate(tetromino: str) -> int:
        """
        :param tetromino: a tetromino name
        :return: The number of rotations possible for the piece
        """
        return len(Consts.ROTATIONS[tetromino])

    @staticmethod
    def get_right(tetromino: str) -> int:
        """
        :param tetromino: a tetromino name
        :return: The number of blocks possible for the piece to move right
        """
        return 5

    @staticmethod
    def get_left(tetromino: str) -> int:
        """
        :param tetromino: a tetromino name
        :return: The number of blocks possible for the piece to move left
        """
        return 5

    @staticmethod
    def get_moves(tetromino: str) -> list[Move]:
        """
        :param tetromino: a tetromino name
        :return: A list of all moves possible for the given tetromino
        """
        moves = []
        for rotate in range(Algorithm.get_rotate(tetromino)):
            moves.append(Move(rotate=rotate))
            for right in range(1, Algorithm.get_right(tetromino)):
                moves.append(Move(right=right, rotate=rotate))
            for left in range(1, Algorithm.get_left(tetromino)):
                moves.append(Move(left=left, rotate=rotate))
        return moves

    @staticmethod
    def calc_score(cells: list[list[str or None]]) -> float:
        """
        Calculate a fitness score for the given board state
        :param cells: a matrix representing the board state
        :return: a fitness score for the current state
        """
        return uniform(-10, 10)

    @staticmethod
    def best_move(cells: list[list[str or None]], cur_tetromino: str, alt_tetromino: str) -> Move:
        board = Board(cells=cells)
        tetromino = Tetromino(name=cur_tetromino)
        best_move_score = -1000000
        best_move = None
        moves = Algorithm.get_moves(cur_tetromino)
        for move in moves:
            for _ in range(move.turn):
                tetromino.rotate_right(board.cells)

            for _ in range(move.right):
                if tetromino.can_move_right(board.cells):
                    tetromino.move_right()

            for _ in range(move.left):
                if tetromino.can_move_left(board.cells):
                    tetromino.move_left()

            board.hard_drop(tetromino)
            board.add_piece(tetromino)
            score = Algorithm.calc_score(board.cells)
            if score > best_move_score:
                best_move_score = score
                best_move = move

            board.cells = cells
            tetromino.__init__(cur_tetromino)

        return best_move

    @staticmethod
    def do_move(cells: list[list[str or None]], cur_tetromino: str, next_tetromino: str,
                held_tetromino: str or None) -> None:
        if held_tetromino is None:
            alt_tetromino = next_tetromino
        else:
            alt_tetromino = held_tetromino
        best_move = Algorithm.best_move(cells, cur_tetromino, alt_tetromino)
        for _ in range(best_move.turn):
            Events.post(Events.rotate_right)

        for _ in range(best_move.right):
            Events.post(Events.move_right)

        for _ in range(best_move.left):
            Events.post(Events.move_left)

        Events.post(Events.hard_drop)


if __name__ == '__main__':
    pass
