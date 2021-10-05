import pygame as pg

from tetris.view.events.event_type import EventType


class CustomEvents:
    RESET_GAME = pg.event.Event(EventType.RESET_GAME.value)
    SWITCH_USE_AI = pg.event.Event(EventType.SWITCH_USE_AI.value)
