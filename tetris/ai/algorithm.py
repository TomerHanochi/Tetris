from random import uniform
from dataclasses import dataclass, field

from tetris.consts import Consts
from tetris.ai.network import Network
from tetris.ai.events import Events
from tetris.model.board import Board
from tetris.model.tetromino import Tetromino


@dataclass(order=True)
class Move:
    rotation: int = field(default=0, compare=False)
    right: int = field(default=0, compare=False)
    left: int = field(default=0, compare=False)
    score: float = field(default=-1000000)


class Algorithm:
    @staticmethod
    def get_rotations(tetromino: str) -> int:
        """
        :param tetromino: a tetromino name
        :return: The number of rotations available for the piece
        """
        return len(Consts.ROTATIONS[tetromino])

    @staticmethod
    def get_right(tetromino: str, rotation: int) -> int:
        """
        :param tetromino: a tetromino name
        :param rotation: current rotation
        :return: The number of blocks possible for the piece to move right
        """
        # the rightmost x index in the rotation
        rightest = max(Consts.ROTATIONS[tetromino][rotation], key=lambda x: x[0])[0]
        return Consts.GRID_WIDTH - (Consts.STARTING_X + rightest)

    @staticmethod
    def get_left(tetromino: str, rotation: int) -> int:
        """
        :param tetromino: a tetromino name
        :param rotation: current rotation
        :return: The number of blocks possible for the piece to move left
        """
        # the leftmost x index in the rotation
        leftest = min(Consts.ROTATIONS[tetromino][rotation], key=lambda x: x[0])[0]
        return Consts.STARTING_X + leftest

    @staticmethod
    def get_moves(tetromino: str) -> list[Move]:
        """
        :param tetromino: a tetromino name
        :return: A list of all moves possible for the given tetromino
        """
        moves = []
        for rotation in range(Algorithm.get_rotations(tetromino)):
            moves.append(Move(rotation=rotation))
            for right in range(1, Algorithm.get_right(tetromino, rotation=rotation)):
                moves.append(Move(right=right, rotation=rotation))
            for left in range(1, Algorithm.get_left(tetromino, rotation=rotation)):
                moves.append(Move(left=left, rotation=rotation))
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
    def score_move(board: Board, tetromino: Tetromino, move: Move) -> float:
        for _ in range(move.rotation):
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

        return score

    @staticmethod
    def best_move(cells: list[list[str or None]], cur_tetromino: str) -> Move:
        board = Board(cells=cells)
        tetromino = Tetromino(name=cur_tetromino)
        best_move = Move()
        moves = Algorithm.get_moves(cur_tetromino)
        for move in moves:
            move.score = Algorithm.score_move(board=board, tetromino=tetromino, move=move)
            if move > best_move:
                best_move = move

            board.cells = cells
            tetromino.__init__(cur_tetromino)

        return best_move

    @staticmethod
    def do_move(cells: list[list[str or None]], cur_tetromino: str, next_tetromino: str,
                held_tetromino: str or None) -> None:
        best_move = Algorithm.best_move(cells, cur_tetromino)
        if held_tetromino is None:
            alt_best_move = Algorithm.best_move(cells, next_tetromino)
        else:
            alt_best_move = Algorithm.best_move(cells, next_tetromino)

        if alt_best_move > best_move:
            Events.post(Events.hold)
            best_move = alt_best_move

        for _ in range(best_move.rotation):
            Events.post(Events.rotate_right)

        for _ in range(best_move.right):
            Events.post(Events.move_right)

        for _ in range(best_move.left):
            Events.post(Events.move_left)

        Events.post(Events.hard_drop)


if __name__ == '__main__':
    pass
