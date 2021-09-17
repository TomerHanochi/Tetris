from tetris.consts import Consts


class GhostTetromino:
    def __init__(self, x: int, y: int, rotation: list[tuple[int, int]]) -> None:
        self.__x = x
        self.__y = y if y > 0 else 0
        self.__rotation = rotation

    def collide_down(self, cells: list[list[str or None]]) -> bool:
        """Any cell under any block is filled"""
        return any(cells[self.y + j + 1][self.x + i] is not None for (i, j) in self.rotation)

    def can_move_down(self, cells: list[list[str or None]]) -> bool:
        """Whether the block is out of bounds or collides with other blocks"""
        return self.y + self.bottommost < Consts.GRID_HEIGHT - 1 and not self.collide_down(cells)

    def move_down(self) -> None:
        self.__y += 1

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def bottommost(self) -> int:
        """Returns the bottommost index in the current rotation"""
        return max(j for (i, j) in self.rotation)

    @property
    def rotation(self) -> list[tuple[int, int]]:
        return self.__rotation
