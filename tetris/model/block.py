from tetris.consts import Consts


class Block:
    def __init__(self, parent: str, i: int, j: int) -> None:
        """
        The base class for the tetrominoes
        :param parent: the name of the parent of the block, used later to get color
        :param i: the x index of the block
        :param j: the y index of the block
        """
        self.parent = parent
        self.__i, self.__j = i, j

    @property
    def can_move_right(self) -> bool:
        return self.__i < Consts.GRID_WIDTH - 1

    def move_right(self) -> None:
        self.__i += 1

    @property
    def can_move_left(self) -> bool:
        return self.__i > 0

    def move_left(self) -> None:
        self.__i -= 1

    @property
    def can_move_down(self) -> bool:
        return self.__j < Consts.GRID_HEIGHT - 1

    def move_down(self) -> None:
        self.__j += 1

    def collide_down(self, other) -> bool:
        return self.i == other.i and self.j + 1 == other.j

    def collide_right(self, other) -> bool:
        return self.j == other.j and self.i + 1 == other.i

    def collide_left(self, other) -> bool:
        return self.j == other.j and self.i - 1 == other.i

    @property
    def in_board(self) -> bool:
        return 0 <= self.__j

    @property
    def i(self) -> int:
        return self.__i

    @i.setter
    def i(self, value: float or int) -> None:
        self.__i = value

    @property
    def j(self) -> int:
        return self.__j

    @j.setter
    def j(self, value: float or int) -> None:
        self.__j = value
