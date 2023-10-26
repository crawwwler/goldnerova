import pygame
import os


image_path = os.path.join(os.path.dirname(__file__), "..", "images", "robot.png")


class Robot:
    def __init__(self):
        self._image = pygame.image.load(image_path)  # robot image
        self._x = 5  # the initial position
        self._y = 300  # "     "       "
        self._toup = False  # robot doesnt move by default
        self._todown = False  # same
        self._toleft = False  # same
        self._toright = False  # same
        self._point = 0  # robot has zero points by default
        self._lives = 9  # robot has 9 lives by default
        self._state = "normal"
        self._collision_time = 0

    # returns robot's image
    @property
    def robot(self):
        return self._image

    # return robot's width position
    @property
    def x(self):
        return self._x

    # return robot's height position
    @property
    def y(self):
        return self._y

    # self._(direction) is by default false,
    # when the up/down/left/right key is pressed this will be true
    @property
    def toup(self):
        return self._toup

    # the method for setting direction value. if up/down/left/right key pressed this will be true
    # and when the key is released , this will be false again
    @toup.setter
    def toup(self, d):
        self._toup = d

    @property
    def todown(self):
        return self._todown

    @todown.setter
    def todown(self, d):
        self._todown = d

    @property
    def toleft(self):
        return self._toleft

    @toleft.setter
    def toleft(self, d):
        self._toleft = d

    @property
    def toright(self):
        return self._toright

    @toright.setter
    def toright(self, d):
        self._toright = d

    # move method, if the conditions evaluate to true , robot moves ( and keep moving until the condition is still true)
    def move(self):
        if self.toup and self.y > 3:
            self._y -= 3
        if self.todown and self.y + self.robot.get_height() < 539:
            self._y += 3
        if self.toleft and self.x > 1:
            self._x -= 3
        if self.toright and self.x + self.robot.get_width() < 799:
            self._x += 3

    # returns the points robot have collected a coin
    @property
    def point(self):
        return self._point

    # when robot collect a coin, this method will be called
    def scored(self):
        if self._point < 20:
            self._point += 1

    # when a ghost hit the robot, this method will be called
    # a coin we be drop and one of the robot's lives will be burned
    def burn(self):
        if self._state == "normal":
            if self._lives > 0:
                self._lives -= 1
            if self._point > 0:
                self._point -= 1
        self._state = "colliding"
        self._collision_time = pygame.time.get_ticks()

    # check if the state of the robot is normal or collided
    # in normal state , robot touching a ghost will result in a life and a point deducted
    def check_state(self):
        if self._state == "colliding":
            elapsed_time = pygame.time.get_ticks() - self._collision_time
            if elapsed_time >= 499:
                self._state = "normal"

    # returns number of robot's lives
    @property
    def life(self):
        return self._lives
