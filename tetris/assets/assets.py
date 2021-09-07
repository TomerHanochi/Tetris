import pygame as pg


class AssetsType(type):
    def __getattr__(cls, item: str) -> tuple[int, int, int] or pg.font.Font:
        try:
            return cls.assets[item]
        except KeyError:
            raise KeyError(f'{item} doesn\'t exist in {cls.__name__}')


class Colors(metaclass=AssetsType):
    assets = {
        'background_color': (0, 0, 0),
        'grid_color': (150, 150, 150),
        'O': (255, 255, 0),
        'I': (0, 255, 255),
        'T': (128, 0, 128),
        'S': (0, 255, 0),
        'Z': (255, 0, 0),
        'L': (0, 0, 255),
        'J': (255, 128, 0),
    }


class Fonts(metaclass=AssetsType):
    if not pg.font.get_init():
        pg.font.init()

    assets = {

    }
