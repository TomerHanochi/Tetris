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
        [(1, 0), (1, 1), (1, 2), (1, 3)],
        [(0, 2), (1, 2), (2, 2), (3, 2)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
    ],
    'T': [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (1, 1), (1, 2), (0, 1)],
    ],
    'S': [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
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
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2), (0, 0)],
    ],
}


class Tetromino:
    def __init__(self, name: str) -> None:
        self.__color = getattr(Colors, name)
        self.__rotations = ROTATIONS[name]
        self.__rotation = 0
        # TODO change starting location of tetrominoes
        self.__x = 0
        self.__y = -4
        self.blocks = [
            Block(self.__x + i, self.__y + j, self.__color) for (i, j) in self.rotation
        ]

    def rotate_right(self) -> None:
        """Rotates the piece right, if rotation is illegal rotates it back"""
        self.__rotation = (self.__rotation + 1) % len(self.__rotations)
        for block, (i, j) in zip(self.blocks, self.rotation):
            block.i = self.__x + i
            block.j = self.__y + j
        if self.leftest.i < 0 or self.rightest.i >= Consts.GRID_WIDTH:
            self.rotate_left()

    def rotate_left(self) -> None:
        """Rotates the piece left, if rotation is illegal rotates it back"""
        self.__rotation = (self.__rotation - 1) % len(self.__rotations)
        for block, (i, j) in zip(self.blocks, self.rotation):
            block.i = self.__x + i
            block.j = self.__y + j
        if self.leftest.i < 0 or self.rightest.i >= Consts.GRID_WIDTH:
            self.rotate_right()

    def can_move_right(self, blocks) -> bool:
        return (self.rightest.can_move_right and
                all(not block.collide_right(other) for other in blocks for block in self.blocks))

    def move_right(self) -> None:
        self.__x += 1
        for block in self.blocks:
            block.move_right()

    def can_move_left(self, blocks) -> bool:
        return (self.leftest.can_move_left and
                all(not block.collide_left(other) for other in blocks for block in self.blocks))

    def move_left(self) -> None:
        self.__x -= 1
        for block in self.blocks:
            block.move_left()

    def can_move_down(self, blocks) -> bool:
        return (all(block.can_move_down for block in self.blocks) and
                all(not block.collide_down(other) for other in blocks for block in self.blocks))

    def move_down(self, speed) -> None:
        self.__y += speed
        for block in self.blocks:
            block.move_down(speed)

    @property
    def rightest(self) -> Block:
        """Returns the rightest index in the current rotation"""
        return max(self.blocks, key=lambda block: block.i)

    @property
    def leftest(self) -> Block:
        """Returns the leftest index in the current rotation"""
        return min(self.blocks, key=lambda block: block.i)

    @property
    def rotation(self) -> list[tuple[int, int]]:
        """Returns the current rotation"""
        return self.__rotations[self.__rotation]
