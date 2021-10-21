from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable

from tetris.consts import Consts
from tetris.ai.network import Network
from tetris.ai.vector import Vector
from tetris.ai.heuristics import Heuristics
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
        :param tetromino: a tetromino name.
        :return: The number of rotations available for the piece.
        """
        return len(Consts.ROTATIONS[tetromino])

    @staticmethod
    def get_right(tetromino: str, rotation: int) -> int:
        """
        :param tetromino: a tetromino name.
        :param rotation: current rotation.
        :return: The number of blocks possible for the piece to move right.
        """
        # the rightmost x index in the rotation
        rightest = max(Consts.ROTATIONS[tetromino][rotation], key=lambda x: x[0])[0]
        return Consts.GRID_WIDTH - (Consts.STARTING_X + rightest) + 1

    @staticmethod
    def get_left(tetromino: str, rotation: int) -> int:
        """
        :param tetromino: a tetromino name.
        :param rotation: current rotation.
        :return: The number of blocks possible for the piece to move left.
        """
        # the leftmost x index in the rotation
        leftest = min(Consts.ROTATIONS[tetromino][rotation], key=lambda x: x[0])[0]
        return Consts.STARTING_X + leftest + 1

    @classmethod
    def get_moves(cls, tetromino: str) -> Iterable[Move]:
        """
        Get all possible moves for a given tetromino
        :param tetromino: a tetromino name.
        :return: A list of all moves possible for the given tetromino.
        """
        for rotation in range(cls.get_rotations(tetromino)):
            # stay in place
            yield Move(rotation=rotation)
            # all moves to the right
            for right in range(1, cls.get_right(tetromino, rotation=rotation)):
                yield Move(right=right, rotation=rotation)
            # all moves to the left
            for left in range(1, cls.get_left(tetromino, rotation=rotation)):
                yield Move(left=left, rotation=rotation)

    @staticmethod
    def calc_score(cells: list[list[str | None]], network: Network) -> float:
        """
        Calculate a fitness score for the given board state.
        :param cells: a matrix representing the board state.
        :param network: a neural network with which to calculate the score.
        :return: a fitness score for the current state.
        """
        inputs = Heuristics.get(cells=[
            [0 if cell is None else 1 for cell in row] for row in cells
        ])
        return network.activate(Vector(inputs))

    @classmethod
    def score_move(cls, board: Board, tetromino: Tetromino, move: Move, network: Network) -> float:
        """
        Does a move on a given board and scores it based on the given neural network.
        :param board: a board with the current board state.
        :param tetromino: a tetromino.
        :param move: a move.
        :param network: a neural network.
        :return: score of the given move.
        """
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
        score = cls.calc_score(board.cells, network)

        return score

    @classmethod
    def best_move(cls, cells: list[list[str | None]], tetromino_name: str, network: Network) -> Move:
        """
        :param cells: the current board state.
        :param tetromino_name: the name of the tetromino.
        :param network: a neural network.
        :return: the best move for the given board state and tetromino.
        """
        board = Board(cells=cells)
        tetromino = Tetromino(name=tetromino_name)
        best_move = Move()
        moves = cls.get_moves(tetromino_name)
        for move in moves:
            move.score = cls.score_move(board, tetromino, move, network)
            if move > best_move:
                best_move = move

            # Restarts the board to its initial state
            board.cells = cells
            tetromino.__init__(tetromino_name)

        return best_move
