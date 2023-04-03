import json

import pygame

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
        if pg.K_ESCAPE in pressed and pressed[pg.K_ESCAPE]:
            self.exit_state()

        self.update_cursor(pressed)
        self.change_player(pressed)

        player_controls = self.game_mgmt.controls_father if self.player == "Father" else self.game_mgmt.controls_son
        for i, control_name in enumerate(player_controls, start=1):
            self.controls_rect[control_name] = None

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
            elif i == self.index + 1 and control_name == self.selected:
                color = "red"
            else:
                color = "green"
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
            self.selected = False
        elif pg.K_UP in pressed and pressed[pg.K_UP]:
            self.index = (self.index - 1) % len(self.game_mgmt.controls_father)
            self.selected = False

    def change_player(self, pressed):
        if pg.K_LEFT in pressed and pressed[pg.K_LEFT] or pg.K_RIGHT in pressed and pressed[pg.K_RIGHT]:
            self.player = "Father" if self.player == "Son" else "Son"
            self.selected = False

    def select(self, pressed):
        if pg.K_RETURN in pressed and pressed[pg.K_RETURN] is True:
            self.selected = list(self.controls_rect.keys())[self.index]

        elif self.selected and pg.K_RETURN in pressed and pressed[pg.K_RETURN] is True:
            self.selected = False

        elif self.selected and pressed and list(pressed.keys())[0] not in [pg.K_RETURN, pg.K_UP, pg.K_DOWN, pg.K_LEFT,
                                                                           pg.K_RIGHT]:
            player_controls = self.game_mgmt.controls_father if self.player == "Father" else self.game_mgmt.controls_son
            key = list(pressed.keys())[0]
            player_controls[self.selected] = key
            self.selected = False

    def new_control(self, pressed):
        if self.selected and pressed and True in pressed.values() and pg.K_RETURN not in pressed.keys():
            print(pressed)
            key = list(pressed)[0]
            if key not in list(self.game_mgmt.controls_father.values()) + list(self.game_mgmt.controls_son.values()):
                player_controls = self.game_mgmt.controls_father if self.player == "Father" \
                    else self.game_mgmt.controls_son
                player_controls[key]
                # print(f"{key} != {list(self.game_mgmt.controls_father.values())} and {list(self.game_mgmt.controls_son.values())}")
