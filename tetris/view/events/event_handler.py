import pygame as pg

from tetris.view.events.event_type import EventType
from tetris.view.events.key import Key
from tetris.view.events.event import Event


class EventHandler:
    @staticmethod
    def get_events() -> list[Event]:
        events = list()
        for event in pg.event.get():
            cur_event_type = None
            for event_type in EventType:
                if event.type == event_type.value:
                    cur_event_type = event_type

            if cur_event_type is not None:
                cur_key = None
                for key in Key:
                    event_key = getattr(event, 'key', None)
                    if event_key == key.value:
                        cur_key = key
                events.append(Event(event_type=cur_event_type, key=cur_key))
        return events
