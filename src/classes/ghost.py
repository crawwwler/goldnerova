import pygame
import math
import os


image_path = os.path.join(os.path.dirname(__file__), "..", "images", "monster.png")


class Ghost:
    # using this class we initialize ghosts which supposed to be in the game
    @classmethod
    def initialize_ghosts(cls):
        list_of_ghosts = []
        list_of_pos_and_crdn = [
            ("top", (4, 44)),
            ("center", (375, 266)),
            ("bottom", (4, 466)),
            ("left", (130, 99)),
            ("right", (620, 99)),
        ]
        for i in range(5):
            g = Ghost(
                list_of_pos_and_crdn[i],
            )
            # print(f"the position of ghost number {i} is {g.x} and {g.y}")
            list_of_ghosts.append(g)
        return list_of_ghosts

    def __init__(self, pos_and_crdn: tuple):
        self._ghost = pygame.image.load(image_path)  # ghost image
        self._id = pos_and_crdn[0]

        # the position of ghosts will be returned by direction method which return a tuple
        # and will be put on x and y
        self._x, self._y = pos_and_crdn[1]

        # initial position of ghosts. using these in move method
        self._startx = self._x
        self._starty = self._y

        self._direction = ""

        self._angle = 0
        self._amplitude = 90
        self._frequency = 0.033

    # returns the ghost image
    @property
    def ghost(self):
        return self._ghost

    @property
    def id(self):
        return self._id

    # return ghost's position
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, d):
        self._x = d

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, d):
        self._y = d

    def set_direction(self, d):
        self._direction = d

    def move_center(self):
        self._angle += self._frequency
        self._x = self._startx + self._amplitude * math.cos(self._angle)
        self._y = self._starty + self._amplitude * math.sin(self._angle)

    def move_top_bottom(self):
        if self._direction == "down":
            self._y += 2.4
        elif self._direction == "up":
            self._y -= 2.4

    def move_left_right(self):
        if self._direction == "right":
            self._x += 2.4
        elif self._direction == "left":
            self._x -= 2.4
