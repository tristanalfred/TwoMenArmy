import json

from states.state import State
from tools import *


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
        self.update_cursor(pressed)
        self.change_player(pressed)
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
        display_text_middle_rect(self.game_mgmt, image.get_rect(topleft=(0, 40)), "<-          CONTROLS          ->")

        player_controls = self.game_mgmt.controls_father if self.player == "Father" else self.game_mgmt.controls_son
        # Display a rectangle for each command
        for i, control_name in enumerate(player_controls, start=1):
            image = pg.Surface((900, 40))
            if i != self.index + 1:
                color = "grey"
            elif i == self.index + 1 and not self.selected:
                color = "white"
            else:
                color = "red"
            image.fill(color)
            self.controls_rect[control_name] = {"image": image, "rect": image.get_rect(topleft=(90, i*80 + 80))}

        # Text for each command
        for action, obj in self.controls_rect.items():
            screen.blit(obj['image'], obj['rect'])
            display_text_middle_rect(
                self.game_mgmt, obj['rect'],
                f"{action}    -    {str.capitalize(pg.key.name(player_controls[action]))}")
        self.controls_rect = {}

    def create_controls_file(self):
        controls = {"TOP_FATHER": 122, "DOWN_FATHER": 115, "LEFT_FATHER": 113, "RIGHT_FATHER": 100,
                    "ATTACK_FATHER": 32, "INTERACTION_FATHER": 101, "PAUSE_FATHER": 112,
                    "TOP_SON": 1073741906, "DOWN_SON": 1073741905, "LEFT_SON": 1073741904, "RIGHT_SON": 1073741903,
                    "ATTACK_SON": 1073741922, "INTERACTION_SON": 1073741913, "PAUSE_SON": 1073741914}

        if not os.path.exists(os.path.join(CURRENT_DIRECTORY, "controls_file.json")):
            with open(os.path.join(CURRENT_DIRECTORY, "controls_file.json"), 'w') as f:
                json.dump(controls, f)

    def read_controls_file(self):
        if os.path.exists(os.path.join(CURRENT_DIRECTORY, "controls_file.json")):
            with open('controls_file.json', 'r') as f:
                json_object = json.load(f)
                self.assign_controls(json_object)

    def assign_controls(self, controls):
        for action, key in controls.items():
            if "FATHER" in action:
                self.game_mgmt.controls_father[action] = key
            else:
                self.game_mgmt.controls_son[action] = key

    def update_cursor(self, pressed):
        if pg.K_DOWN in pressed and pressed[pg.K_DOWN]:
            self.index = (self.index + 1) % len(self.game_mgmt.controls_father)
        elif pg.K_UP in pressed and pressed[pg.K_UP]:
            self.index = (self.index - 1) % len(self.game_mgmt.controls_father)

    def change_player(self, pressed):
        if pg.K_LEFT in pressed and pressed[pg.K_LEFT] or pg.K_RIGHT in pressed and pressed[pg.K_RIGHT]:
            self.player = "Father" if self.player == "Son" else "Son"

    def select(self, pressed):
        if pg.K_RETURN in pressed and pressed[pg.K_RETURN]:
            self.selected = not self.selected
