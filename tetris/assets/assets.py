from os.path import abspath
import pygame as pg

from tetris.utils.consts import Consts


class AssetsType(type):
    def __getattr__(cls, item: str) -> tuple[int, int, int] or pg.font.Font:
        try:
            return cls.assets[item]
        except KeyError:
            raise KeyError(f'{item} doesn\'t exist in {cls.__name__}')


class Loader:
    @staticmethod
    def load_image(path: str, width: int or float, height: int or float):
        return pg.transform.smoothscale(
            pg.image.load(path), (int(width), int(height))
        )

    @staticmethod
    def load_font(path: str, size: int or float):
        return pg.font.Font(path, size)


class Colors(metaclass=AssetsType):
    assets = {
        'background': (0, 0, 0),
        'title': (255, 255, 255),
        'cub_title': (255, 255, 255),
        'default_text': (255, 255, 255),
        'O': (255, 255, 0),
        'I': (0, 255, 255),
        'T': (128, 0, 128),
        'S': (0, 255, 0),
        'Z': (255, 0, 0),
        'L': (0, 0, 255),
        'J': (255, 128, 0),
    }


class Images(metaclass=AssetsType):
    base_path = abspath('tetris/assets/images')
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


class Fonts(metaclass=AssetsType):
    base_path = abspath('tetris/assets/fonts')
    assets = {
        'title': Loader.load_font(f'{base_path}/pixel.ttf', Consts.BLOCK_SIZE * 2),
        'sub_title': Loader.load_font(f'{base_path}/pixel.ttf', Consts.BLOCK_SIZE),
    }
