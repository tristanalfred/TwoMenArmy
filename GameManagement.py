import json
import sys
from states.title import Title
from tools import *


class GameManagement:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.state_stack = []
        self.title_screen = None
        self.pressed = {}
        self.clock = pg.time.Clock()  # FPS management
        self.text_font_screen = pg.font.SysFont("georgia", 50)
        self.text_font_object = pg.font.SysFont("georgia", 36)
        self.load_states()
        self.controls_father = {}
        self.controls_son = {}

        self.create_controls_files()
        self.read_controls_file()

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
            elif event.type == pg.KEYDOWN:
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

    def create_controls_files(self):
        controls_father = {TOP: pg.K_z, DOWN: pg.K_s, LEFT: pg.K_q, RIGHT: pg.K_d, "attack": pg.K_SPACE,
                           "interaction": pg.K_e, "pause": pg.K_ESCAPE}
        controls_son = {TOP: pg.K_UP, DOWN: pg.K_DOWN, LEFT: pg.K_LEFT, RIGHT: pg.K_RIGHT, "attack": pg.K_KP0,
                        "interaction": pg.K_KP1, "pause": pg.K_KP2}

        # Create father control file
        if not os.path.exists(os.path.join(HOME_DIRECTORY, CONTROLS_FILE_FATHER)):
            with open(os.path.join(HOME_DIRECTORY, CONTROLS_FILE_FATHER), 'w') as f:
                json.dump(controls_father, f)

        # Create son control file
        if not os.path.exists(os.path.join(HOME_DIRECTORY, CONTROLS_FILE_SON)):
            with open(os.path.join(HOME_DIRECTORY, CONTROLS_FILE_SON), 'w') as f:
                json.dump(controls_son, f)

    def read_controls_file(self):
        if os.path.exists(os.path.join(HOME_DIRECTORY, CONTROLS_FILE_FATHER)):
            with open(CONTROLS_FILE_FATHER, 'r') as f:
                json_object = json.load(f)
                for action, key in json_object.items():
                    self.controls_father[action] = key

        if os.path.exists(os.path.join(HOME_DIRECTORY, CONTROLS_FILE_SON)):
            with open(CONTROLS_FILE_SON, 'r') as f:
                json_object = json.load(f)
            for action, key in json_object.items():
                self.controls_son[action] = key

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
