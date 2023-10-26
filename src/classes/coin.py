import pygame
from random import randint
import os


images_path = os.path.join(os.path.dirname(__file__), "..", "images", "coin.png")


class Coin:
    def __init__(self):
        self._image = pygame.image.load(images_path)  # coin image

        # positions that coins could be appeared
        self._y = randint(4, 540 - self._image.get_height())

        # because of the door in the bottom right corner we have to check
        # if a coin doesnt appear on the position that door located
        if self._y > 500:
            self._x = randint(4, 760 - self._image.get_width())
        else:
            self._x = randint(4, 790 - self._image.get_width())

    @property
    def image(self):
        return self._image

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
