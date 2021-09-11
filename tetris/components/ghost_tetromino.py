from tetris.components.block import Block


class GhostTetromino:
    def __init__(self, tetromino, blocks) -> None:
        self.blocks = [
            Block('ghost', tetromino.x + i, tetromino.y + j)
            for (i, j) in tetromino.rotation
        ]
        while self.can_move_down(blocks):
            for block in self.blocks:
                block.move_down()

    def can_move_down(self, blocks) -> bool:
        return (all(block.can_move_down for block in self.blocks) and
                all(not block.collide_down(other) for other in blocks for block in self.blocks))

    def update(self, tetromino, blocks) -> None:
        for block, (i, j) in zip(self.blocks, tetromino.rotation):
            block.i = i + tetromino.x
            block.j = j + tetromino.y

        while self.can_move_down(blocks):
            for block in self.blocks:
                block.move_down()
