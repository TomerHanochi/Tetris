from __future__ import annotations

import pygame as pg

from tetris.consts import Consts
from tetris.view.assets import Images


class Context:
    @staticmethod
    def window() -> pg.Surface:
        """Returns the current display"""
        return pg.display.get_surface()

    @staticmethod
    def mouse_pos() -> tuple[float, float]:
        return pg.mouse.get_pos()

    @staticmethod
    def fill(x: float, y: float, w: float, h: float, color: tuple[int, int, int]) -> None:
        """
        :param x: top left x coordinate
        :param y: top left y coordinate
        :param w: width of the filled area
        :param h: height of the filled area
        :param color: fill color
        """
        Context.window().fill(color, (x, y, w, h))

    @staticmethod
    def image(x: float, y: float, image: pg.Surface):
        """
        :param x: top left x coordinate
        :param y: top left y coordinate
        :param image: an image to draw
        """
        Context.window().blit(image, (x, y))

    @staticmethod
    def tetromino(x: float, y: float, rotation: list[tuple[int, int]],
                  name: str) -> None:
        """
        :param x: top left x coordinate
        :param y: top left y coordinate
        :param rotation: the tetromino's current rotation
        :param name: the name of the tetromino to get its block image
        """
        image = getattr(Images, name)
        for (i, j) in rotation:
            Context.image(image=image,
                          x=(x + i * Consts.BLOCK_SIZE), y=(y + j * Consts.BLOCK_SIZE))

    @staticmethod
    def border(x: float, y: float, width: int, height: int) -> None:
        """
        :param x: top left x coordinate
        :param y: top left y coordinate
        :param width: the number of blocks in width
        :param height: the number of blocks in height
        """
        image = Images.border
        for i in range(width):
            pos_x, pos_y = x + i * Consts.BLOCK_SIZE, y
            Context.image(pos_x, pos_y, image)
            Context.image(pos_x, pos_y + (height - 1) * Consts.BLOCK_SIZE, image)
        # offset by -2 to avoid drawing the corners twice
        for j in range(height - 2):
            pos_x, pos_y = x, y + (j + 1) * Consts.BLOCK_SIZE
            Context.image(pos_x, pos_y, image)
            Context.image(pos_x + (width - 1) * Consts.BLOCK_SIZE, pos_y, image)
