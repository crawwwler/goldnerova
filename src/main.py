""" 
    This game is for 'Mooc Fi' python course 2023, as final exercise.
    First i wanted to thank all the people involved in this course And, 
    members of CS department of University of Helsinki. Amazing 
    course, it did wonders for me!
    
    The game Goldnerova includes :
    - a screen for title and description and rules
    - a game screen which is the playground and it contains an scoreboard
    - a notification page for winning and gameover
    - a menu screen

    How to play :
      player should control a robot using arrowkeys and trying to 
      collect coins to reach the goal (20 coins) while avoiding the
      flying ghosts entering the game from different angles. 
      After the player reached the goal, the robot should be guided to
      the door which is the final stage of the game. Bumping into ghosts
      more than 9 times is the gameover to make sure game will finish at
      some point in case the player being so bad at it.
    
    There is a Menu screen in game which is pretty simple and letting the user
    exits the game or restarts it.  Completing the game will take 30-90 
    seconds.
    ps. hope you do have the font i used for texts - its name is 
    Showcard Gothic apparently - otherwise with default font it gonna look dead!
      """


import pygame
import os
from classes.goldnerova import Goldnerova
from classes.robot import Robot

# from classes.ghost import Ghost
from classes.door import Door
from classes.coin import Coin

image_robot = os.path.join(os.path.dirname(__file__), "images", "robot.png")
image_ghost = os.path.join(os.path.dirname(__file__), "images", "monster.png")


class Menu:
    def __init__(self):
        self.robot = pygame.image.load(image_robot)  # robot image
        self.ghost = pygame.image.load(image_ghost)  # ghost image

        # the fonts we need in menu
        self.fonts = {
            64: pygame.font.SysFont("Showcard Gothic", 64),
            38: pygame.font.SysFont("Showcard Gothic", 38),
            16: pygame.font.SysFont("Showcard Gothic", 16),
            10: pygame.font.SysFont("Showcard Gothic", 10),
        }

    # first page of the game
    def welcome(self, window: pygame.surface.Surface):
        check = True  # used for ensure the welcome page displayed at right time
        # AN IMPORTANT ASPECT OF THIS METHOD AND THE WHILE LOOP IN IT IS
        # THERE'S NO CODE OUTSIDE THE LOOP
        # SO IF THE CHECK IS FALSE
        # CODE RETURN TO WHERE welcome METHOD HAS BEEN CALLED
        # WHICH IS IN GOLDNEROVA CLASS
        while check:
            # pygame.event.get() returns a queue of the events happening in game
            for event in pygame.event.get():
                # pygame.QUIT is when user click on X button of the window (top right corner usually)
                if event.type == pygame.QUIT:
                    exit()

                # checking if event type is pressing a key
                if event.type == pygame.KEYDOWN:
                    # checking if the pressing key is the enter key, here it is named RETURN
                    if event.key == pygame.K_RETURN:
                        # if enter key is pressed , we will enter the game, so check is false and no more welcome page
                        check = False
                        # adding an event key so when the key esc is pressed
                        # exit() executed
                        # added @oct24 -- testing
                    if event.key == pygame.K_ESCAPE:
                        exit()

            # the appearence of welcome page
            window.fill((101, 11, 101))  # color
            # txt is the title of the game, content, antialiasing , text color, background color
            txt = self.fonts[64].render("GOLDNEROVA", True, (233, 222, 0), (0, 0, 0))

            # with blit method, we want to copy the source surface - here it is txt -
            # to target surface - here the window - , and in plus , second parameter
            # is the coordinates of the position we want the surface being displayed.
            window.blit(txt, (400 - txt.get_width() / 2, 120 - txt.get_height() / 2))
            # RULES AND DESCRIPTION
            SCRIPT = r"""A NASA robot agent has landed on planet Goldnerova 
            for a few minutes
            the objectives of the exploration are very simple:
            1.  Avoid the Goldnerova local ghosts! bumping into each flying 
            ghosts will cause you one life damage and a coin drop
            2.  bring back a total of 20 gold coin with yourself to spaceship
            3.  use the arrowkeys to play
            4.  you only have 9 lives to complete the mission
                enjoy your time on goldnerova!"""

            desc_y = 180
            # spliting the rules into a list , and iterating over the list
            for line in SCRIPT.split("\n"):
                desc = self.fonts[16].render(line, True, (233, 222, 0), (0, 0, 0))
                window.blit(desc, (110, desc_y))
                desc_y += desc.get_height() + 6

            # design things xd , twelve ghosts in welcome page, we have positions of ghosts
            # in a dict here
            ghost_pos = {
                0: (14, 29),
                1: (266, 444),
                2: (575, 50),
                3: (79, 503),
                4: (704, 499),
                5: (30, 190),
                6: (699, 118),
                7: (444, 510),
                8: (70, 366),
                9: (710, 300),
                10: (704, 33),
                11: (304, 9),
            }

            # iterating a range, 0 - 11 , ghost_pos[i] is a tuple of ghost position
            for i in range(12):
                window.blit(self.ghost, ghost_pos[i])

            pe = self.fonts[38].render(
                "PRESS ENTER TO START!", True, (233, 222, 0), (0, 0, 0)
            )
            window.blit(pe, (400 - pe.get_width() / 2, 400))

            # this is for updating contents of the game window
            pygame.display.flip()

    # design of the page for when user won the game
    def winner(self, window: pygame.surface.Surface):
        window.fill((221, 0, 0))
        txt = self.fonts[64].render(
            "YOU WON!",
            True,
            (
                0,
                0,
                0,
            ),
        )
        window.blit(txt, (400 - txt.get_width() / 2, 130))

        window.blit(self.robot, (400 - self.robot.get_width() / 2, 304))
        # drawing circles // design purposes
        pygame.draw.circle(window, (255, 255, 255), (424, 292), 4)
        pygame.draw.circle(window, (255, 255, 255), (432, 286), 5)
        pygame.draw.circle(window, (255, 255, 255), (452, 260), 25)
        rich = self.fonts[10].render("I'm rich", True, (0, 0, 0))
        window.blit(rich, (433, 255))
        # pressing esc at winning or losing page will redirect you to end page
        restart = self.fonts[16].render(
            "[esc] for restart or exit", True, (233, 222, 0), (0, 0, 0)
        )
        window.blit(restart, (400 - restart.get_width() / 2, 550))
        pygame.display.flip()

    def end(self, window: pygame.surface.Surface):
        check = True
        while check:
            # checking events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        exit()
                    if event.key == pygame.K_n:
                        check = False
            window.fill((101, 11, 101))
            to_quit = self.fonts[38].render("Press [Y] to Quit", True, (0, 0, 0))
            window.blit(to_quit, (400 - to_quit.get_width() / 2, 200))
            pr_esc = self.fonts[38].render("Press [N] for new game", True, (0, 0, 0))
            window.blit(pr_esc, (400 - pr_esc.get_width() / 2, 400))
            pygame.display.flip()
        # if y key pressed, we quit the loop and calling the start function which is
        # welcome page to start a new game
        start(1)

    # method for when user lose the game
    def game_over(self, window: pygame.surface.Surface):
        window.fill((0, 0, 221))
        txt = self.fonts[64].render("GAME OVER!", True, (0, 0, 0))
        window.blit(txt, (400 - txt.get_width() / 2, 130))
        window.blit(self.ghost, (400 - self.robot.get_width() / 2, 304))
        pygame.draw.circle(window, (255, 255, 255), (424, 292), 4)
        pygame.draw.circle(window, (255, 255, 255), (432, 286), 5)
        pygame.draw.circle(window, (255, 255, 255), (452, 260), 25)
        loser = self.fonts[10].render("BOO!", True, (0, 0, 0))
        window.blit(loser, (435, 255))
        restart = self.fonts[16].render(
            "[esc] for restart or exit", True, (233, 222, 0), (0, 0, 0)
        )
        window.blit(restart, (400 - restart.get_width() / 2, 550))
        pygame.display.flip()


def start(x: int):
    # putting an instance of these class into the variables and passing the variables to main class
    r = Robot()
    c = Coin()
    d = Door()
    m = Menu()
    if x == 1:
        Goldnerova(r, c, d, m)  # this is a class but we didnt assign it to any variable
    else:
        return


pygame.init()  # initialize pygame
start(
    1
)  # the logic here is to pass the start func a 1 so the game main function begin executed
