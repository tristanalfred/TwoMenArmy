import sys
from global_variables import *
from states.title import Title
from tools import *


class GameManagement:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.pause = False
        self.state_stack = []
        self.title_screen = None
        self.pressed = {}
        self.clock = pg.time.Clock()  # FPS management
        self.text_font_screen = pg.font.SysFont("georgia", 50)
        self.text_font_object = pg.font.SysFont("georgia", 36)
        self.load_states()

    def handling_events(self):
        """
        Get all the events, like key pressed
        """
        for event in pg.event.get():
            # Close the game
            if event.type == pg.QUIT:
                self.running = False
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_KP2:
                self.pause = not self.pause
            elif event.type == pg.KEYDOWN and not self.pause:
                self.pressed[event.key] = True
            elif event.type == pg.KEYUP:
                self.pressed[event.key] = False

    def update(self):
        """
        Update the state of the game and entities (ex : move a player)
        """
        self.state_stack[-1].update(self.pressed)

    def display(self):
        """
        Display all the entities on the screen
        """
        self.state_stack[-1].display(self.screen)
        pg.display.flip()

    def reset_keys(self):
        self.pressed = {}

    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)

    def run(self):
        self.handling_events()
        self.update()
        self.display()
        self.clock.tick(FPS)
