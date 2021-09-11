from random import randint

from tetris.components.block import Block
from tetris.utils.consts import Consts


class Tetromino:
    def __init__(self, name: str) -> None:
        self.__name = name
        self.__rotations = Consts.ROTATIONS[name]
        self.__rotation = 0
        a, b = Consts.STARTING_POSITIONS[name]
        self.__x = randint(a, b)
        self.__y = -2
        self.blocks = [
            Block(name, self.__x + i, self.__y + j) for (i, j) in self.rotation
        ]

    def rotate_right(self) -> None:
        """Rotates the piece right, if rotation is illegal rotates it back"""
        self.__rotation = (self.__rotation + 1) % len(self.__rotations)
        for block, (i, j) in zip(self.blocks, self.rotation):
            block.i = self.__x + i
            block.j = self.__y + j
        if self.leftmost.i < 0 or self.rightmost.i >= Consts.GRID_WIDTH:
            self.rotate_left()

    def rotate_left(self) -> None:
        """Rotates the piece left, if rotation is illegal rotates it back"""
        self.__rotation = (self.__rotation - 1) % len(self.__rotations)
        for block, (i, j) in zip(self.blocks, self.rotation):
            block.i = self.__x + i
            block.j = self.__y + j
        if self.leftmost.i < 0 or self.rightmost.i >= Consts.GRID_WIDTH:
            self.rotate_right()

    def can_move_right(self, blocks) -> bool:
        return (self.rightmost.can_move_right and
                all(not block.collide_right(other) for other in blocks for block in self.blocks))

    def move_right(self) -> None:
        self.__x += 1
        for block in self.blocks:
            block.move_right()

    def can_move_left(self, blocks) -> bool:
        return (self.leftmost.can_move_left and
                all(not block.collide_left(other) for other in blocks for block in self.blocks))

    def move_left(self) -> None:
        self.__x -= 1
        for block in self.blocks:
            block.move_left()

    def can_move_down(self, blocks) -> bool:
        return (all(block.can_move_down for block in self.blocks) and
                all(not block.collide_down(other) for other in blocks for block in self.blocks))

    def move_down(self) -> None:
        self.__y += 1
        for block in self.blocks:
            block.move_down()

    @property
    def rightmost(self) -> Block:
        """Returns the rightmost index in the current rotation"""
        return max(self.blocks, key=lambda block: block.i)

    @property
    def leftmost(self) -> Block:
        """Returns the leftmost index in the current rotation"""
        return min(self.blocks, key=lambda block: block.i)

    @property
    def topmost(self) -> Block:
        """Returns the topmost index in the current rotation"""
        return min(self.blocks, key=lambda block: block.j)

    @property
    def bottommost(self) -> Block:
        """Returns the bottommost index in the current rotation"""
        return max(self.blocks, key=lambda block: block.j)

    @property
    def rotation(self) -> list[tuple[int, int]]:
        """Returns the current rotation"""
        return self.__rotations[self.__rotation]

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def width(self) -> int:
        return abs(self.x - self.rightmost.i)

    @property
    def height(self) -> int:
        return abs(self.y - self.bottommost.j)

    @property
    def name(self) -> str:
        return self.__name
