from enum import Enum

from pygame import (K_RIGHT, K_LEFT, K_UP, K_DOWN, K_SPACE, KMOD_CTRL,
                    KMOD_SHIFT, K_c, K_z, K_x, K_ESCAPE)


class Key(Enum):
    RIGHT_ARROW = K_RIGHT
    LEFT_ARROW = K_LEFT
    UP_ARROW = K_UP
    DOWN_ARROW = K_DOWN
    SPACE_BAR = K_SPACE
    CONTROL = KMOD_CTRL
    SHIFT = KMOD_SHIFT
    ESCAPE = K_ESCAPE
    C = K_c
    X = K_x
    Z = K_z
