import pygame as pg

from tetris.consts import Consts
from tetris.assets.assets import Images


class Draw:
    @staticmethod
    def image(x: int, y: int, image: pg.Surface):
        """Draws an image in coordinates (x, y) on the current screen"""
        pg.display.get_surface().blit(image, (x, y))

    @staticmethod
    def tetromino(x: int, y: int, rotation: list[tuple[int, int]],
                  name: str) -> None:
        for (i, j) in rotation:
            Draw.image(image=getattr(Images, name),
                       x=x + i * Consts.BLOCK_SIZE, y=y + i * Consts.BLOCK_SIZE)

    @staticmethod
    def border(width: int, height: int) -> None:
