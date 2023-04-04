import json
from states.state import State
from tools import *


INTERFACE_CONTROLS = [pg.K_RETURN, pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT]


class ControlsMenu(State):
    def __init__(self, game_mgmt):
        State.__init__(self, game_mgmt)
        self.game_mgmt = game_mgmt
        self.controls_rect = {}
        self.index = 0
        self.selected = False
        self.player = "Father"

        self.create_controls_file()
        self.read_controls_file()

    def update(self, pressed):
        if pg.K_ESCAPE in pressed and pressed[pg.K_ESCAPE]:
            self.exit_state()

        self.update_cursor(pressed)
        self.change_player(pressed)
        self.load_player_controls()
        self.select(pressed)
        self.game_mgmt.reset_keys()

    def display(self, screen):
        self.game_mgmt.state_stack[-3].display(screen)
        display_grey_filter(screen)

        # Tile of controls menu
        image = pg.Surface((1080, 40))
        color = "white"
        image.fill(color)
        screen.blit(image, image.get_rect(topleft=(0, 40)))
        display_text_middle_rect(
            self.game_mgmt,
            image.get_rect(topleft=(0, 40)), f"<-          CONTROLS   {str.upper(self.player)}         ->")

        # Display a rectangle for each command
        player_controls = self.game_mgmt.controls_father if self.player == "Father" else self.game_mgmt.controls_son
        for i, control_name in enumerate(player_controls, start=1):
            image = pg.Surface((900, 40))
            if i != self.index + 1:
                color = "grey"
            elif i == self.index + 1 and not self.selected:
                color = "white"
            elif i == self.index + 1 and control_name == self.selected:
                color = "red"
            else:
                color = "green"  # Not supposed to happen
            image.fill(color)
            self.controls_rect[control_name] = {"image": image, "rect": image.get_rect(topleft=(90, i*80 + 80))}

        # Text for each command
        for action, obj in self.controls_rect.items():
            screen.blit(obj['image'], obj['rect'])
            display_text_middle_rect(
                self.game_mgmt, obj['rect'],
                f"{action.split(' ')[0]}    -    {str.capitalize(pg.key.name(player_controls[action]))}")
        self.controls_rect = {}

    def load_player_controls(self):
        """
        Load the controls of the correct player to be used until the other one is selected
        """
        player_controls = self.game_mgmt.controls_father if self.player == "Father" else self.game_mgmt.controls_son
        for i, control_name in enumerate(player_controls, start=1):
            self.controls_rect[control_name] = None

    def create_controls_file(self):
        controls = {"TOP FATHER": 122, "DOWN FATHER": 115, "LEFT FATHER": 113, "RIGHT FATHER": 100,
                    "ATTACK FATHER": 32, "INTERACTION FATHER": 101, "PAUSE FATHER": 112,
                    "TOP SON": 1073741906, "DOWN SON": 1073741905, "LEFT SON": 1073741904, "RIGHT SON": 1073741903,
                    "ATTACK SON": 1073741922, "INTERACTION SON": 1073741913, "PAUSE SON": 1073741914}

        if not os.path.exists(os.path.join(CURRENT_DIRECTORY, CONTROLS_FILE)):
            with open(os.path.join(CURRENT_DIRECTORY, CONTROLS_FILE), 'w') as f:
                json.dump(controls, f)

    def read_controls_file(self):
        if os.path.exists(os.path.join(CURRENT_DIRECTORY, CONTROLS_FILE)):
            with open('controls_file.json', 'r') as f:
                json_object = json.load(f)
                self.assign_initial_controls(json_object)

    def assign_initial_controls(self, controls):
        for action, key in controls.items():
            if "FATHER" in action:
                self.game_mgmt.controls_father[action] = key
            else:
                self.game_mgmt.controls_son[action] = key

    def update_cursor(self, pressed):
        if pg.K_DOWN in pressed and pressed[pg.K_DOWN]:
            self.index = (self.index + 1) % len(self.game_mgmt.controls_father)
            self.selected = False
        elif pg.K_UP in pressed and pressed[pg.K_UP]:
            self.index = (self.index - 1) % len(self.game_mgmt.controls_father)
            self.selected = False

    def change_player(self, pressed):
        if pg.K_LEFT in pressed and pressed[pg.K_LEFT] or pg.K_RIGHT in pressed and pressed[pg.K_RIGHT]:
            self.player = "Father" if self.player == "Son" else "Son"
            self.selected = False

    def select(self, pressed):
        # Select the control to change
        if pg.K_RETURN in pressed and pressed[pg.K_RETURN] is True:
            self.selected = list(self.controls_rect.keys())[self.index]

        # Deselect if enter is pressed again
        elif self.selected and pg.K_RETURN in pressed and pressed[pg.K_RETURN] is True:
            self.selected = False

        # Change the control selected
        elif self.selected and pressed and list(pressed.keys())[0] not in INTERFACE_CONTROLS:
            player_controls = self.game_mgmt.controls_father if self.player == "Father" else self.game_mgmt.controls_son
            key = list(pressed.keys())[0]
            player_controls[self.selected] = key
            self.selected = False
