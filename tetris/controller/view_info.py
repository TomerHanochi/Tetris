from tetris.model.model import Model
from tetris.consts import Consts


class ViewInfo:
    def __init__(self, model: Model) -> None:
        self.cur_tetromino = model.cur_tetromino.name
        self.cur_tetromino_x = model.cur_tetromino.x
        self.cur_tetromino_y = model.cur_tetromino.y
        self.cur_tetromino_rotation = [(i, j) for i, j in model.cur_tetromino.rotation
                                       if model.cur_tetromino.y + j >= 0]
        self.next_tetrominoes = model.next_tetrominoes
        self.held_tetromino = model.held_tetromino
        self.ghost_tetromino_x = model.ghost_tetromino.x
        self.ghost_tetromino_y = model.ghost_tetromino.y
        self.ghost_tetromino_rotation = model.ghost_tetromino.rotation
        self.blocks = [(i, j, cell)
                       for j, row in enumerate(model.board.cells) for i, cell in enumerate(row)
                       if cell is not None]
        self.high_score = model.high_score
        self.score = model.score
        self.cleared = model.cleared
        self.level = model.level
        self.paused = model.paused
        self.pause_cooldown = model.pause_cooldown
        self.pause_cooldown_in_seconds = self.pause_cooldown // Consts.FRAME_RATE + 1
