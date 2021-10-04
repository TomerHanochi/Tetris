from __future__ import annotations

from tetris.view.events.event_type import EventType
from tetris.view.events.key import Key


class Event:
    def __init__(self, event_type: EventType, key: Key = None) -> None:
        self.__type = event_type
        self.__key = key

    @property
    def type(self) -> EventType:
        return self.__type

    @property
    def key(self) -> Key:
        return self.__key

    def __str__(self) -> str:
        return f'type={self.type}, key={self.__key}'
