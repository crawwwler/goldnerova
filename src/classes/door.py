import pygame
import os


image_path = os.path.join(os.path.dirname(__file__), "..", "images", "spaceship.png")


class Door:
    def __init__(self):
        self._image = pygame.image.load(image_path)  # door image
        self._x = 808 - self._image.get_width()  # door position
        self._y = 545 - self._image.get_height()

    @property
    def image(self):
        return self._image

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
