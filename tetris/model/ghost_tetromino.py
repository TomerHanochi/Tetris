from tetris.model.block import Block
from tetris.consts import Consts


class GhostTetromino:
    def __init__(self, x: int, rotation: list[tuple[int, int]], blocks: list[Block]) -> None:
        self.__x = x
        self.__y = Consts.STARTING_POSITION[1]
        self.__rotation = rotation
        self.__blocks = [
            Block('ghost', i, j) for (i, j) in rotation
        ]
        self.move_down(blocks)

    def collide_down(self, blocks: list[Block]) -> bool:
        return any(self.y + block.j == other.j - 1 and self.x + block.i == other.i
                   for other in blocks for block in self.blocks)

    def can_move_down(self, blocks: list[Block]) -> bool:
        return self.y + self.bottommost < Consts.GRID_HEIGHT - 1 and not self.collide_down(blocks)

    def move_down(self, blocks) -> None:
        while self.can_move_down(blocks):
            self.__y += 1

    def update(self, x: int, rotation: list[tuple[int, int]], blocks: list[Block]):
        self.__x = x
        self.__y = Consts.STARTING_POSITION[1]
        self.__rotation = rotation
        for block, (i, j) in zip(self.blocks, rotation):
            block.i = i
            block.j = j
        self.move_down(blocks)

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def bottommost(self) -> int:
        """Returns the bottommost index in the current rotation"""
        return max((block.j for block in self.blocks))

    @property
    def blocks(self) -> list[Block]:
        return self.__blocks

    @property
    def rotation(self) -> list[tuple[int, int]]:
        return self.__rotation
