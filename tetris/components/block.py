class Block:
    def __init__(self, i: int, j: int, color: tuple[int, int, int]) -> None:
        self.i, self.j = i, j
        self.color = color

    @property
    def in_board(self) -> bool:
        return 0 <= self.j
