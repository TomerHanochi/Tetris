from tetris.components.block import Block
from tetris.assets.assets import Colors

ROTATIONS = {
    # TODO Enter rotations of tetrominoes
    'O': [
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        # [(), (), (), ()],
        # [(), (), (), ()],
        # [(), (), (), ()],
    ],
    # 'I': [
    #     [(), (), (), ()],
    #     [(), (), (), ()],
    #     [(), (), (), ()],
    #     [(), (), (), ()],
    # ],
    # 'T': [
    #     [(), (), (), ()],
    #     [(), (), (), ()],
    #     [(), (), (), ()],
    #     [(), (), (), ()],
    # ],
    # 'S': [
    #     [(), (), (), ()],
    #     [(), (), (), ()],
    #     [(), (), (), ()],
    #     [(), (), (), ()],
    # ],
    # 'Z': [
    #     [(), (), (), ()],
    #     [(), (), (), ()],
    #     [(), (), (), ()],
    #     [(), (), (), ()],
    # ],
    # 'L': [
    #     [(), (), (), ()],
    #     [(), (), (), ()],
    #     [(), (), (), ()],
    #     [(), (), (), ()],
    # ],
    # 'J': [
    #     [(), (), (), ()],
    #     [(), (), (), ()],
    #     [(), (), (), ()],
    #     [(), (), (), ()],
    # ],
}


class Tetromino:
    def __init__(self, name) -> None:
        self.__color = getattr(Colors, name)
        self.__x = 0  # TODO change starting location of tetrominoes
        self.__rotations = ROTATIONS[name]
        self.__rotation = 0
        self.blocks = [
            Block(i, j - 4, self.__color) for (i, j) in self.rotation
        ]

    def rotate_right(self) -> None:
        """Rotates the piece right, if rotation is illegal rotates it back"""
        self.__rotation = (self.__rotation + 1) % len(self.__rotations)
        if self.leftest < 0 or self.rightest > 9:
            self.rotate_left()
        else:
            for block, (i, j) in zip(self.blocks, self.rotation):
                block.i = i
                block.j = j

    def rotate_left(self) -> None:
        """Rotates the piece left, if rotation is illegal rotates it back"""
        self.__rotation = (self.__rotation - 1) % len(self.__rotations)
        if self.leftest < 0 or self.rightest > 9:
            self.rotate_right()
        else:
            for block, (i, j) in zip(self.blocks, self.rotation):
                block.i = i
                block.j = j

    def move_down(self) -> None:
        """Moves the tetromino one block down"""
        for block in self.blocks:
            block.j += 1

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
