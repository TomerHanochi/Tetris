from tetris.model.block import Block


class GhostTetromino:
    def __init__(self, tetromino, blocks) -> None:
        """
        The hint tetromino that shows where the current tetromino will fall
        :param tetromino: the current tetromino
        :param blocks: all blocks currently in the board
        """
        self.blocks = [
            Block('ghost', tetromino.x + i, tetromino.y + j)
            for (i, j) in tetromino.rotation
        ]

        # drops it to where the current tetromino will land
        while self.can_move_down(blocks):
            for block in self.blocks:
                block.move_down()

    def can_move_down(self, blocks) -> bool:
        """
        Whether the ghost can move down, used to drop it to the where the current
        tetromino will land
        """
        return (all(block.can_move_down for block in self.blocks) and
                all(not block.collide_down(other) for other in blocks for block in self.blocks))

    def update(self, tetromino, blocks) -> None:
        """
        Updates the ghost tetromino to reflect the current state of the board
        :param tetromino: the current tetromino
        :param blocks: all blocks currently in the board
        """
        for block, (i, j) in zip(self.blocks, tetromino.rotation):
            block.i = i + tetromino.x
            block.j = j + tetromino.y

        # drops it to where the current tetromino will land
        while self.can_move_down(blocks):
            for block in self.blocks:
                block.move_down()
