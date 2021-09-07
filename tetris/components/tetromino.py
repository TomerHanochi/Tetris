from tetris.components.block import Block
from tetris.assets.assets import Colors
from tetris.utils.consts import Consts

ROTATIONS = {
    # The rotations are taken from the fan made,
    # but still trustworthy, TetrisWiki - https://tetris.fandom.com/wiki/SRS
    'O': [
        [(0, 0), (1, 0), (0, 1), (1, 1)],
    ],
    'I': [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
        [(0, 2), (1, 2), (2, 2), (3, 2)],
        [(1, 0), (1, 1), (1, 2), (1, 3)],
    ],
    'T': [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (1, 1), (1, 2), (0, 1)],
    ],
    'S': [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 1), (2, 1), (0, 2), (1, 2)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
    ],
    'Z': [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 2), (2, 2)],
        [(1, 0), (1, 1), (0, 1), (0, 2)],
    ],
    'L': [
        [(0, 1), (1, 1), (2, 1), (0, 0)],
        [(1, 0), (1, 1), (1, 2), (2, 0)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (1, 2), (0, 2)],
    ],
    'J': [
        [(0, 1), (1, 1), (2, 1), (2, 0)],
        [(1, 0), (1, 1), (1, 2), (0, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2), (0, 0)],
    ],
}


class Tetromino:
    def __init__(self, name: str) -> None:
        self.__color = getattr(Colors, name)
        self.__rotations = ROTATIONS[name]
        self.__rotation = 0
        offset = 0  # TODO change starting location of tetrominoes
        self.blocks = [
            Block(i, j, self.__color) for (i, j) in self.rotation
        ]

    def rotate_right(self) -> None:
        """Rotates the piece right, if rotation is illegal rotates it back"""
        self.__rotation = (self.__rotation + 1) % len(self.__rotations)
        if self.leftest < 0 or self.rightest >= Consts.GRID_WIDTH:
            self.rotate_left()
        else:
            for block, (i, j) in zip(self.blocks, self.rotation):
                block.i = i
                block.j = j

    def rotate_left(self) -> None:
        """Rotates the piece left, if rotation is illegal rotates it back"""
        self.__rotation = (self.__rotation - 1) % len(self.__rotations)
        if self.leftest < 0 or self.rightest >= Consts.GRID_WIDTH:
            self.rotate_right()
        else:
            for block, (i, j) in zip(self.blocks, self.rotation):
                block.i = i
                block.j = j

    def can_move_right(self, blocks) -> bool:
        return (self.rightest < Consts.GRID_WIDTH - 1 and
                all(not block.collide_right(other) for other in blocks for block in self.blocks))

    def move_right(self) -> None:
        for block in self.blocks:
            block.move_right()

    def can_move_left(self, blocks) -> bool:
        return (self.leftest > 0 and
                all(not block.collide_left(other) for other in blocks for block in self.blocks))

    def move_left(self) -> None:
        for block in self.blocks:
            block.move_left()

    def can_move_down(self, blocks) -> bool:
        return (all(block.j < Consts.GRID_HEIGHT - 1 for block in self.blocks) and
                all(not block.collide_down(other) for other in blocks for block in self.blocks))

    def move_down(self, speed) -> None:
        for block in self.blocks:
            block.move_down(speed)

    @property
    def rightest(self) -> int:
        """Returns the rightest index in the current rotation"""
        return max(self.blocks, key=lambda block: block.i).i

    @property
    def leftest(self) -> int:
        """Returns the leftest index in the current rotation"""
        return min(self.blocks, key=lambda block: block.i).i

    @property
    def rotation(self) -> list[tuple[int, int]]:
        """Returns the current rotation"""
        return self.__rotations[self.__rotation]

