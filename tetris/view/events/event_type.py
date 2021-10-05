from enum import Enum

from pygame import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, QUIT, event


class EventType(Enum):
    KEY_DOWN = KEYDOWN
    KEY_UP = KEYUP
    MOUSE_CLICKED = MOUSEBUTTONDOWN
    QUIT = QUIT
    RESET_GAME = event.custom_type()
    SWITCH_USE_AI = event.custom_type()
