class Consts:
    """
    Class of constant values used throughout the game
    Used to make sure there is no need to scour files to change constants
    """
    SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 1000
    BLOCK_SIZE = 40
    GRID_WIDTH = 10
    GRID_HEIGHT = 20
    FRAME_RATE = 60
    # the frames before the player can move horizontally
    HORIZONTAL_COOLDOWN = 6
    # the frames before the player can soft drop
    SOFT_DROP_COOLDOWN = int(FRAME_RATE / 20)
    # the frames before the tetromino moves down, differs by level
    COOLDOWN_BY_LEVEL = (48, 43, 38, 33, 28, 23, 18, 13, 8, 6, 5, 5, 5,
                         4, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1)
    # the multiplier for clearing 1-4 rows at once, respectively
    ROW_CLEAR_MULT = (40, 100, 300, 1200)
    # the multiplier per cell for hard dropping a tetromino
    HARD_DROP_MULT = 2
    # the multiplier per cell for soft dropping a tetromino
    SOFT_DROP_MULT = 1
    # the number of next tetrominoes displayed
    NEXT_SET_SIZE = 3
    # all the rotations relative to the tetrominoes position
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
    Y_OFFSET = -4
    TETROMINO_NAMES = ROTATIONS.keys()
