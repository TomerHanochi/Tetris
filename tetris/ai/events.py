import pygame as pg


class Events:
    """ Events class used to make library switching easier. """
    @staticmethod
    def post(event_: pg.event.Event) -> None:
        pg.event.post(event_)

    AI_MOVE = pg.event.custom_type()

    move_right = pg.event.Event(AI_MOVE, key=pg.K_RIGHT)
    move_left = pg.event.Event(AI_MOVE, key=pg.K_LEFT)
    hard_drop = pg.event.Event(AI_MOVE, key=pg.K_SPACE)
    hold = pg.event.Event(AI_MOVE, key=pg.K_c)
    rotate_right = pg.event.Event(AI_MOVE, key=pg.K_x)
    rotate_left = pg.event.Event(AI_MOVE, key=pg.K_z)
