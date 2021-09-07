class Block:
    def __init__(self, i: float, j: float, color: tuple[int, int, int]) -> None:
        self.__i, self.__j = i, j
        self.__color = color

    def move_right(self) -> None:
        self.__i += 1

    def move_left(self) -> None:
        self.__i -= 1

    def move_down(self, speed) -> None:
        self.__j += speed

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
    def color(self) -> tuple[int, int, int]:
        return self.__color

    @property
    def i(self) -> int:
        return int(self.__i)

    @i.setter
    def i(self, value: float or int) -> None:
        self.__i = value

    @property
    def j(self) -> int:
        return int(self.__j)

    @j.setter
    def j(self, value: float or int) -> None:
        self.__j = value
