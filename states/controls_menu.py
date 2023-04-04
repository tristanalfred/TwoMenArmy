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
        self.player = FATHER

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
        player_controls = self.game_mgmt.controls_father if self.player == FATHER else self.game_mgmt.controls_son
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
        player_controls = self.game_mgmt.controls_father if self.player == FATHER else self.game_mgmt.controls_son
        for i, control_name in enumerate(player_controls, start=1):
            self.controls_rect[control_name] = None

    def update_cursor(self, pressed):
        if pg.K_DOWN in pressed and pressed[pg.K_DOWN]:
            self.index = (self.index + 1) % len(self.game_mgmt.controls_father)
            self.selected = False
        elif pg.K_UP in pressed and pressed[pg.K_UP]:
            self.index = (self.index - 1) % len(self.game_mgmt.controls_father)
            self.selected = False

    def change_player(self, pressed):
        if pg.K_LEFT in pressed and pressed[pg.K_LEFT] or pg.K_RIGHT in pressed and pressed[pg.K_RIGHT]:
            self.player = FATHER if self.player == SON else SON
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
            player_controls = self.game_mgmt.controls_father if self.player == FATHER else self.game_mgmt.controls_son
            key = list(pressed.keys())[0]
            player_controls[self.selected] = key
            self.selected = False
            self.save_new_controls()

    def save_new_controls(self):
        if self.player == FATHER:
            with open(os.path.join(HOME_DIRECTORY, CONTROLS_FILE_FATHER), 'w') as f:
                json.dump(self.game_mgmt.controls_father, f)
        else:
            with open(os.path.join(HOME_DIRECTORY, CONTROLS_FILE_SON), 'w') as f:
                json.dump(self.game_mgmt.controls_son, f)
