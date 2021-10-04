from enum import Enum

from pygame import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, QUIT, event


class EventType(Enum):
    KEY_DOWN = KEYDOWN
    KEY_UP = KEYUP
    MOUSE_CLICKED = MOUSEBUTTONDOWN
    QUIT = QUIT
