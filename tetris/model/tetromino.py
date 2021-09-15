from random import randint

from tetris.model.block import Block
from tetris.consts import Consts


class Tetromino:
    def __init__(self, name: str) -> None:
        """
        A tetromino is a geometric shape built by 4 blocks.
        their name correspond to their shape
        :param name: the name of the tetromino, used to decide its rotations
                     and starting position
        """
        self.__name = name
        self.__rotations = Consts.ROTATIONS[name]
        self.__rotation = 0
        a, b = Consts.STARTING_POSITIONS[name]
        self.__x = randint(a, b)
        # the default y position is just above the board, by default
        self.__y = Consts.Y_OFFSET
        self.__blocks = [
            Block(name, i, j) for (i, j) in self.rotation
        ]

    @property
    def out_of_bounds(self) -> bool:
        return self.x + self.leftmost < 0 or self.x + self.rightmost >= Consts.GRID_WIDTH

    def overlap(self, blocks: list[Block]) -> bool:
        return any(self.x + block.i == other.i and self.y + block.j == other.j
                   for other in blocks for block in self.blocks)

    def rotate_right(self, blocks: list[Block]) -> None:
        """Rotates the piece right, if rotation is illegal rotates it back"""
        self.__rotation = (self.__rotation + 1) % len(self.__rotations)
        for block, (i, j) in zip(self.blocks, self.rotation):
            block.i = i
            block.j = j
        if self.out_of_bounds or self.overlap(blocks):
            self.rotate_left(blocks)

    def rotate_left(self, blocks: list[Block]) -> None:
        """Rotates the piece left, if rotation is illegal rotates it back"""
        self.__rotation = (self.__rotation - 1) % len(self.__rotations)
        for block, (i, j) in zip(self.blocks, self.rotation):
            block.i = i
            block.j = j
        if self.out_of_bounds or self.overlap(blocks):
            self.rotate_right(blocks)

    def collide_right(self, blocks: list[Block]) -> bool:
        return any(self.x + block.i == other.i - 1 and self.y + block.j == other.j
                   for other in blocks for block in self.blocks)

    def can_move_right(self, blocks: list[Block]) -> bool:
        return self.x + self.rightmost < Consts.GRID_WIDTH - 1 and not self.collide_right(blocks)

    def move_right(self) -> None:
        self.__x += 1

    def collide_left(self, blocks: list[Block]) -> bool:
        return any(self.x + block.i == other.i + 1 and self.y + block.j == other.j
                   for other in blocks for block in self.blocks)

    def can_move_left(self, blocks: list[Block]) -> bool:
        return self.x + self.leftmost > 0 and not self.collide_left(blocks)

    def move_left(self) -> None:
        self.__x -= 1

    def collide_down(self, blocks: list[Block]) -> bool:
        return any(self.y + block.j == other.j - 1 and self.x + block.i == other.i
                   for other in blocks for block in self.blocks)

    def can_move_down(self, blocks: list[Block]) -> bool:
        return self.y + self.bottommost < Consts.GRID_HEIGHT - 1 and not self.collide_down(blocks)

    def move_down(self) -> None:
        self.__y += 1

    @property
    def rightmost(self) -> int:
        """Returns the rightmost index in the current rotation"""
        return max((block.i for block in self.blocks))

    @property
    def leftmost(self) -> int:
        """Returns the leftmost index in the current rotation"""
        return min((block.i for block in self.blocks))

    @property
    def topmost(self) -> int:
        """Returns the topmost index in the current rotation"""
        return min((block.j for block in self.blocks))

    @property
    def bottommost(self) -> int:
        """Returns the bottommost index in the current rotation"""
        return max((block.j for block in self.blocks))

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
        return abs(self.leftmost - self.rightmost) + 1

    @property
    def height(self) -> int:
        return abs(self.topmost - self.bottommost) + 1

    @property
    def name(self) -> str:
        return self.__name

    @property
    def blocks(self) -> list[Block]:
        return self.__blocks
