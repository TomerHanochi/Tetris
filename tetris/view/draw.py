import pygame as pg

from tetris.consts import Consts
from tetris.assets.assets import Images


class Draw:
    @staticmethod
    def window() -> pg.Surface:
        """Returns the current display"""
        return pg.display.get_surface()

    @staticmethod
    def image(x: int, y: int, image: pg.Surface):
        """
        :param x: top left x coordinate
        :param y: top left y coordinate
        :param image: an image to draw
        """
        Draw.window().blit(image, (x, y))

    @staticmethod
    def tetromino(x: int, y: int, rotation: list[tuple[int, int]],
                  name: str) -> None:
        """
        :param x: top left x coordinate
        :param y: top left y coordinate
        :param rotation: the tetromino's current rotation
        :param name: the name of the tetromino to get its block image
        """
        image = getattr(Images, name)
        for (i, j) in rotation:
            Draw.image(image=image,
                       x=(x + i * Consts.BLOCK_SIZE), y=(y + j * Consts.BLOCK_SIZE))

    @staticmethod
    def border(x: int, y: int, width: int, height: int) -> None:
        """
        :param x: top left x coordinate
        :param y: top left y coordinate
        :param width: the number of blocks in width
        :param height: the number of blocks in height
        """
        image = getattr(Images, 'border')
        for i in range(width):
            pos_x, pos_y = x + i * Consts.BLOCK_SIZE, y
            Draw.image(pos_x, pos_y, image)
            Draw.image(pos_x, pos_y + (height - 1) * Consts.BLOCK_SIZE, image)
        # offset by -2 to avoid drawing the corners twice
        for j in range(height - 2):
            pos_x, pos_y = x, y + (j + 1) * Consts.BLOCK_SIZE
            Draw.image(pos_x, pos_y, image)
            Draw.image(pos_x + (width - 1) * Consts.BLOCK_SIZE, pos_y, image)
