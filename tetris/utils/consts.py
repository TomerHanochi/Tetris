class Consts:
    SCREEN_SIZE = 1200, 1000
    FRAME_RATE = 60
    HORIZONTAL_COOLDOWN = 4
    VERTICAL_COOLDOWN = 4
    BLOCK_SIZE = 40
    GRID_WIDTH = 10
    GRID_HEIGHT = 20
    NEXT_SET_SIZE = 3
    ROTATIONS = {
        'O': (
            ((0, 0), (1, 0), (0, 1), (1, 1)),
        ),
        'I': (
            ((0, 1), (1, 1), (2, 1), (3, 1)),
            ((1, 0), (1, 1), (1, 2), (1, 3)),
            ((0, 2), (1, 2), (2, 2), (3, 2)),
            ((2, 0), (2, 1), (2, 2), (2, 3)),
        ),
        'T': (
            ((1, 0), (0, 1), (1, 1), (2, 1)),
            ((1, 0), (1, 1), (2, 1), (1, 2)),
            ((0, 1), (1, 1), (2, 1), (1, 2)),
            ((1, 0), (1, 1), (1, 2), (0, 1)),
        ),
        'S': (
            ((1, 0), (2, 0), (0, 1), (1, 1)),
            ((1, 0), (1, 1), (2, 1), (2, 2)),
            ((1, 1), (2, 1), (0, 2), (1, 2)),
            ((0, 0), (0, 1), (1, 1), (1, 2)),
        ),
        'Z': (
            ((0, 0), (1, 0), (1, 1), (2, 1)),
            ((2, 0), (1, 1), (2, 1), (1, 2)),
            ((0, 1), (1, 1), (1, 2), (2, 2)),
            ((1, 0), (1, 1), (0, 1), (0, 2)),
        ),
        'L': (
            ((0, 1), (1, 1), (2, 1), (0, 0)),
            ((1, 0), (1, 1), (1, 2), (2, 0)),
            ((0, 1), (1, 1), (2, 1), (2, 2)),
            ((1, 0), (1, 1), (1, 2), (0, 2)),
        ),
        'J': (
            ((0, 1), (1, 1), (2, 1), (2, 0)),
            ((1, 0), (1, 1), (1, 2), (2, 2)),
            ((0, 1), (1, 1), (2, 1), (0, 2)),
            ((1, 0), (1, 1), (1, 2), (0, 0)),
        ),
    }
    STARTING_POSITIONS = {
        'O': (3, 6),
        'I': (3, 6),
        'T': (0, 4),
        'S': (0, 4),
        'Z': (0, 4),
        'L': (0, 4),
        'J': (0, 4),
    }
    TETROMINO_NAMES = ROTATIONS.keys()
