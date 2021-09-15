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
    def i(self) -> int:
        return self.__i

    @i.setter
    def i(self, i: int) -> None:
        if not isinstance(i, int):
            raise ValueError(f'Wrong variable type: {type(i).__name__} should\'ve been int')
        self.__i = i

    @property
    def j(self) -> int:
        return self.__j

    @j.setter
    def j(self, j: int) -> None:
        if not isinstance(j, int):
            raise ValueError(f'Wrong variable type: {type(j).__name__} should\'ve been int')
        self.__j = j
