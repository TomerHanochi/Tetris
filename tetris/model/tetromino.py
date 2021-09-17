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
        self.__x, self.__y = Consts.STARTING_POSITION
        self.__y = 0

    @property
    def out_of_bounds(self) -> bool:
        return self.x + self.leftmost < 0 or self.x + self.rightmost >= Consts.GRID_WIDTH

    def overlap(self, cells: list[list[str or None]]) -> bool:
        return any(cells[self.x + i][self.y + j] is not None for (i, j) in self.rotation)

    def rotate_right(self, cells: list[list[str or None]]) -> None:
        """Rotates the piece right, if rotation is illegal rotates it back"""
        self.__rotation = (self.__rotation + 1) % len(self.__rotations)
        if self.out_of_bounds or self.overlap(cells):
            self.rotate_left(cells)

    def rotate_left(self, cells: list[list[str or None]]) -> None:
        """Rotates the piece left, if rotation is illegal rotates it back"""
        self.__rotation = (self.__rotation - 1) % len(self.__rotations)
        if self.out_of_bounds or self.overlap(cells):
            self.rotate_right(cells)

    def collide_right(self, cells: list[list[str or None]]) -> bool:
        return any(cells[self.x + i + 1][self.y + j] is not None for (i, j) in self.rotation)

    def can_move_right(self, cells: list[list[str or None]]) -> bool:
        return self.x + self.rightmost < Consts.GRID_WIDTH - 1 and not self.collide_right(cells)

    def move_right(self) -> None:
        self.__x += 1

    def collide_left(self, cells: list[list[str or None]]) -> bool:
        return any(cells[self.x + i - 1][self.y + j] is not None for (i, j) in self.rotation)

    def can_move_left(self, cells: list[list[str or None]]) -> bool:
        return self.x + self.leftmost > 0 and not self.collide_left(cells)

    def move_left(self) -> None:
        self.__x -= 1

    def collide_down(self, cells: list[list[str or None]]) -> bool:
        return any(cells[self.x + i][self.y + j + 1] is not None for (i, j) in self.rotation)

    def can_move_down(self, cells: list[list[str or None]]) -> bool:
        return self.y + self.bottommost < Consts.GRID_HEIGHT - 1 and not self.collide_down(cells)

    def move_down(self) -> None:
        self.__y += 1

    @property
    def rightmost(self) -> int:
        """Returns the rightmost index in the current rotation"""
        return max(i for (i, j) in self.rotation)

    @property
    def leftmost(self) -> int:
        """Returns the leftmost index in the current rotation"""
        return min(i for (i, j) in self.rotation)

    @property
    def topmost(self) -> int:
        """Returns the topmost index in the current rotation"""
        return min(j for (i, j) in self.rotation)

    @property
    def bottommost(self) -> int:
        """Returns the bottommost index in the current rotation"""
        return max(j for (i, j) in self.rotation)

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
