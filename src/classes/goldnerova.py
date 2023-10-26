import pygame
import os
from .ghost import Ghost
from .coin import Coin

background_path = os.path.join(
    os.path.dirname(__file__), "..", "images", "background.jpg"
)
background_init = pygame.image.load(background_path)
background = pygame.transform.scale(background_init, (800, 600))


class Goldnerova:
    def __init__(self, robot, cc, door, menu):
        self.player = robot
        self.window = pygame.display.set_mode((800, 600))  # the size for window game
        pygame.display.set_caption("GOLDNEROVA")  # caption of the window
        # below, create an cock object. used to control the frame rate of game loop
        self.clock = (
            pygame.time.Clock()
        )  # put an object instance of CLOCK class into the self.clock
        self.font = pygame.font.SysFont("Showcard Gothic", 26)
        self.target = cc  # coin
        # self.enemy = []  # ghosts
        self.enemy = Ghost.initialize_ghosts()
        self.door = door
        self.menu = menu
        # very soon we will undestand what the fuck are these three variables below
        self.scored = False  # i dont have any explanation for this, i cant remember, but i left it in the code anyway
        self.game_won = False
        self.dead = False
        self.__x = 0  # esc pressed assign this 1 value
        # DISPLAYING POINT OF VIEW SPEAKING , THIS IS WHERE OUR GAME STARTED.
        # WE PASS THE GAME WINDOW TO WELCOME METHOD OF THE MENU CLASS
        # ( ACTUALLY THE OBJECT OF THE MENU CLASS WHICH WE PUT IN self.menu)
        # CALLING IT
        self.menu.welcome(self.window)
        # THIS IS THE MAIN LOOP OF THE GAME
        # THE CODE WILL BE STAYED IN THIS LOOP UNTIL OF ONE THE CONDITIONS
        # NEEDED FOR GAME TO BE ENDED REACHED, OR THE USER QUITS THE GAME
        self.main_loop()
        # end method of menu is called only when user press esc during the game
        # or after the game, pressing esc stopping the main loop of the game.
        self.menu.end(self.window)

    def event_handler(self):
        # iterating over event queues
        for event in pygame.event.get():
            # if event is clicking on X button on top right corner of window (usually), then exit() function getting called
            # meaning window will be closed
            if event.type == pygame.QUIT:
                exit()

            # if event is pressing up, down, left or right arrowkeys,
            # relevent method getting called (method offered by robot class obv)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.toup = True
                if event.key == pygame.K_DOWN:
                    self.player.todown = True
                if event.key == pygame.K_LEFT:
                    self.player.toleft = True
                if event.key == pygame.K_RIGHT:
                    self.player.toright = True
                # if event is pressing esc key, the __x is 1 ,
                # which causes the while loop in main loop method stop executing
                # and end method of menu gets called
                if event.key == pygame.K_ESCAPE:
                    self.__x = 1

            # when user release the key , it is an event
            # and we call the same method but giving them the false as parameter
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.player.toup = False
                if event.key == pygame.K_DOWN:
                    self.player.todown = False
                if event.key == pygame.K_LEFT:
                    self.player.toleft = False
                if event.key == pygame.K_RIGHT:
                    self.player.toright = False

    # the main method of the game
    def update_game(self):
        # checking if the user reached the necessary condition to win the game
        if self.game_solved():
            self.game_won = True
            return

        # checking if the user still able to continue the game, if not game over
        if self.death():
            self.dead = True
            return
        # CALLING MOVE METHOD OF ROBOT OBJECT -PLAYER- ,, CALLING IT DOESNT NECESSARILY MEANING
        # THAT THE ROBOT WILL MOVE, BECAUSE USER HAVE TO PRESS ONE OF THE ARROWKEYS SO ONE OF THE
        # EXISTING CONDITION IN THE CALLED METHOD EVALUATES TO TRUE (ASSUMING OTHER FACTOR IS ALREADY THERE)
        self.player.move()

        # HERE, WE HAVE OUR BACKGROUND YELLOW
        # IT IS ABSOLUTELY NECESSARY TO CALLING THIS FUCNTION DURING THE GAME
        self.window.blit(background, (0, 0))

        # drawing the line which is separating the playground from scoreboard
        pygame.draw.line(self.window, (0, 0, 0), (0, 540), (800, 540), 3)

        # rendering the scoreboard and assign it to a variable , so we can use it in blit function
        # as a source surface that we want to copy to target surface which is window
        scoreboard = self.font.render(
            f"Coins: {self.player.point}  Lives:  {self.player.life}",
            True,
            (101, 11, 101),
            (0, 0, 0),
        )

        # copying source surface to target surface
        self.window.blit(scoreboard, (22, 570 - scoreboard.get_height() / 2))

        # rendering instruction
        instruction = self.font.render(
            "[esc] exit / new game", True, (101, 11, 101), (0, 0, 0)
        )

        # copying instruction to target surface
        self.window.blit(instruction, (500, 570 - instruction.get_height() / 2))

        # rendring door sign which when the player reach enough points
        # will apear on the screen and pointing to the door
        doorsign = self.font.render("RUN TO DOOR >>>", True, (233, 222, 0), (0, 0, 0))

        # check the condition , if user collected enough coins ?
        if self.player.point == 20:
            # if yes, then doorsign will copy to target surface (window)
            self.window.blit(
                doorsign, (755 - doorsign.get_width(), 530 - doorsign.get_height())
            )

        # copying the image of elements of the game to window
        self.window.blit(self.player.robot, (self.player.x, self.player.y))
        self.window.blit(self.target.image, (self.target.x, self.target.y))
        self.window.blit(self.door.image, (self.door.x, self.door.y))

        # THIS IS THE LOGIC FOR ROBOT COLLECTING A COIN
        # IF ANY SPOT OF A ROBOT TOUCHES A COIN THEN COIN IS COLLECTED
        if (
            self.player.x < self.target.x + self.target.image.get_width()
            and self.player.x + self.player.robot.get_width() > self.target.x
            and self.player.y < self.target.y + self.target.image.get_height()
            and self.player.y + self.player.robot.get_height() > self.target.y
        ):
            # player is scored. calling scored method means points + 1
            self.player.scored()
            # calling makecoin() next, cause we need the next target
            self.target = self.makecoin()
            # no idea what the below assignment and generally self.scored is. but i will leave this here
            self.scored = True

        for ghost in self.enemy:
            # new logic
            if ghost.id in ["top", "bottom"]:
                if ghost.x <= 4:
                    ghost.set_direction("right")
                elif ghost.x >= 790 - ghost.ghost.get_width():
                    ghost.set_direction("left")
                ghost.move_left_right()
            elif ghost.id in ["left", "right"]:
                if ghost.y <= 99:
                    ghost.set_direction("down")
                elif ghost.y >= 401:
                    ghost.set_direction("up")
                ghost.move_top_bottom()
            elif ghost.id == "center":
                ghost.move_center()

            # copying the source surface (ghost image) to target surface (window)
            self.window.blit(ghost.ghost, (ghost.x, ghost.y))

            # same as logic for scoring and arriving at door,
            # if any part of the robot touches any part of the ghost
            # two points will be dropped and a life too
            if (
                self.player.x < ghost.x + ghost.ghost.get_width()
                and self.player.x + self.player.robot.get_width() > ghost.x
                and self.player.y < ghost.y + ghost.ghost.get_height()
                and self.player.y + self.player.robot.get_height() > ghost.y
            ):
                self.player.burn()  # a life dropped => (self._lives of robot instance - 1)

        # checking the collision state of player
        self.player.check_state()
        # update the contents of main surface
        pygame.display.flip()
        # control the frame rate @60 FPS
        self.clock.tick(60)

    # the logic is simple, if any spot of the robot touches the door,
    # in case the robot collected atleast 20 coins, then game is won by user
    def game_solved(self):
        if (
            self.player.x < self.door.x + self.door.image.get_width()
            and self.player.x + self.player.robot.get_width() > self.door.x
            and self.player.y < self.door.y + self.door.image.get_height()
            and self.player.y + self.player.robot.get_height() > self.door.y
        ) and self.player.point == 20:
            return True
        return False

    # death or game over. when user has no life remained, the game is over
    def death(self):
        if self.player.life == 0:
            return True
        return False

    # this one is a bit tricky. we call it we robot collected a coin, so we need the next target
    # the coin returned by this method will be asigned to self.target
    def makecoin(self):
        self.scored = False
        return Coin()

    def main_loop(self):
        # __x is 0, unless user press the esc key
        while self.__x == 0:
            # calling event handler
            self.event_handler()
            # checking if the user won the game
            if self.game_won:
                # calling the method for winner page of menu class
                self.menu.winner(self.window)
            # check if the user lost the game
            elif self.dead:
                # calling the loser page of menu game
                self.menu.game_over(self.window)
            # otherwise calling update_game method, which is -kinda- the method operating the game
            else:
                self.update_game()
