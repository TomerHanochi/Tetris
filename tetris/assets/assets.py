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


class Colors(metaclass=AssetsType):
    assets = {
        'background_color': (0, 0, 0),
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
        'L': Loader.load_image(f'{base_path}/Blue.png', Consts.BLOCK_SIZE, Consts.BLOCK_SIZE),
        'J': Loader.load_image(f'{base_path}/Orange.png', Consts.BLOCK_SIZE, Consts.BLOCK_SIZE),
        'ghost': Loader.load_image(f'{base_path}/Ghost.png', Consts.BLOCK_SIZE, Consts.BLOCK_SIZE),
        'border': Loader.load_image(f'{base_path}/Border.png', Consts.BLOCK_SIZE, Consts.BLOCK_SIZE),
        'title': Loader.load_image(f'{base_path}/Title.png', Consts.BLOCK_SIZE * Consts.GRID_WIDTH,
                                   Consts.BLOCK_SIZE * Consts.GRID_WIDTH * .25),
    }
