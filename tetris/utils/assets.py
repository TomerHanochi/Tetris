import pygame as pg


class AssetsType(type):
    def __getattr__(cls, item: str) -> tuple[int, int, int] or pg.font.Font:
        try:
            return cls.assets[item]
        except KeyError:
            raise KeyError(f'{item} doesn\'t exist in {cls!s}')


class Colors(metaclass=AssetsType):
    assets = {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
    }


class Fonts(metaclass=AssetsType):
    if not pg.font.get_init():
        pg.font.init()

    assets = {

    }
