from __future__ import annotations

import pygame as pg

from tetris.consts import Consts


class Assets(type):
    """
    Metaclass used to retrieve data from the assets classes.
    this is so instead of writing Colors.assets['background'] you can just write Colors.background.
    """
    def __getattr__(cls, item: str) -> tuple[int, int, int] | pg.font.Font | pg.Surface:
        try:
            return cls.assets[item]
        except KeyError:
            raise KeyError(f'{item} doesn\'t exist in {cls.__name__}')


class Loader:
    """
    A basic loader class used to load fonts and images.
    Used so there is only one place that needs to be changed.
    """
    @staticmethod
    def load_image(path: str, width: int | float, height: int | float) -> pg.Surface:
        return pg.transform.smoothscale(
            pg.image.load(path), (int(width), int(height))
        )

    @staticmethod
    def load_font(path: str, size: int | float) -> pg.font.Font:
        return pg.font.Font(path, int(size))

    @staticmethod
    def load_sound(path: str) -> pg.mixer.Sound:
        return pg.mixer.Sound(path)


class Colors(metaclass=Assets):
    """ An assets class that has all the colors. """
    assets = {
        'background': (0, 0, 0),
        'title': (255, 255, 255),
        'sub_title': (255, 255, 255),
        'statistic': (255, 255, 255),
        'button_background': (0, 0, 0),
        'button_text': (255, 255, 255),
    }


class Images(metaclass=Assets):
    """ An assets class with all of the images. """
    base_path = f'{Consts.BASE_PATH}/assets/images'
    assets = {
        'O': Loader.load_image(f'{base_path}/Yellow.png', Consts.BLOCK_SIZE, Consts.BLOCK_SIZE),
        'I': Loader.load_image(f'{base_path}/LightBlue.png', Consts.BLOCK_SIZE, Consts.BLOCK_SIZE),
        'T': Loader.load_image(f'{base_path}/Purple.png', Consts.BLOCK_SIZE, Consts.BLOCK_SIZE),
        'S': Loader.load_image(f'{base_path}/Green.png', Consts.BLOCK_SIZE, Consts.BLOCK_SIZE),
        'Z': Loader.load_image(f'{base_path}/Red.png', Consts.BLOCK_SIZE, Consts.BLOCK_SIZE),
        'J': Loader.load_image(f'{base_path}/Blue.png', Consts.BLOCK_SIZE, Consts.BLOCK_SIZE),
        'L': Loader.load_image(f'{base_path}/Orange.png', Consts.BLOCK_SIZE, Consts.BLOCK_SIZE),
        'ghost': Loader.load_image(f'{base_path}/Ghost.png', Consts.BLOCK_SIZE, Consts.BLOCK_SIZE),
        'border': Loader.load_image(f'{base_path}/Border.png', Consts.BLOCK_SIZE, Consts.BLOCK_SIZE),
        'title': Loader.load_image(f'{base_path}/Title.png', Consts.BLOCK_SIZE * Consts.GRID_WIDTH,
                                   Consts.BLOCK_SIZE * Consts.GRID_WIDTH * .25),
    }


class Fonts(metaclass=Assets):
    """ An assets class with all of the fonts. """
    base_path = f'{Consts.BASE_PATH}/assets/fonts'
    assets = {
        'title': Loader.load_font(f'{base_path}/pixel.ttf', Consts.BLOCK_SIZE * 2),
        'sub_title': Loader.load_font(f'{base_path}/pixel.ttf', Consts.BLOCK_SIZE),
        'statistic': Loader.load_font(f'{base_path}/pixel.ttf', Consts.BLOCK_SIZE * .8),
        'button': Loader.load_font(f'{base_path}/pixel.ttf', Consts.BLOCK_SIZE),
    }


class Sounds(metaclass=Assets):
    """
    An assets class with all of the sounds
    """
    base_path = f'{Consts.BASE_PATH}/assets/sounds'
    assets = {
        'music': Loader.load_sound(f'{base_path}/music.mp3'),
    }
