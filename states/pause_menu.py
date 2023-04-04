from states.state import State
from states.controls_menu import ControlsMenu
from tools import *


class PauseMenu(State):
    def __init__(self, game_mgmt):
        State.__init__(self, game_mgmt)
        self.game_mgmt = game_mgmt
        # Set the menu
        self.options_rect = {}
        # Set the cursor and menu states
        self.menu_options = {0: "Controls", 1: "Exit"}
        self.index = 0

    def update(self, pressed):
        self.update_cursor(pressed)
        if pg.K_RETURN in pressed and pressed[pg.K_RETURN]:
            self.transition_state()
        if pg.K_ESCAPE in pressed and pressed[pg.K_ESCAPE]:
            self.exit_state()
        self.game_mgmt.reset_keys()

    def display(self, screen):
        # render the gameworld behind the menu, which is right before the pause menu on the stack
        # self.game.state_stack[-2].display(display)
        self.prev_state.display(screen)
        display_grey_filter(screen)

        # Display Menu title
        image = pg.Surface((1080, 40))
        color = "white"
        image.fill(color)
        screen.blit(image, image.get_rect(topleft=(0, 40)))
        display_text_middle_rect(
            self.game_mgmt,
            image.get_rect(topleft=(0, 40)), "MENU")

        # Display a command for each option
        for i, option_name in self.menu_options.items():
            image = pg.Surface((900, 40))
            if i != self.index:
                color = "grey"
            else:
                color = "white"
            image.fill(color)
            self.options_rect[option_name] = {"image": image, "rect": image.get_rect(topleft=(90, (i+1)*80 + 80))}

        # Text for each option
            for action, obj in self.options_rect.items():
                screen.blit(obj['image'], obj['rect'])
                display_text_middle_rect(self.game_mgmt, obj['rect'], action)
            self.options_rect = {}

    def transition_state(self):
        if self.menu_options[self.index] == "Controls":
            new_state = ControlsMenu(self.game_mgmt)
            new_state.enter_state()
        elif self.menu_options[self.index] == "Exit":
            while len(self.game_mgmt.state_stack) > 1:
                self.game_mgmt.state_stack.pop()

    def update_cursor(self, pressed):
        if pg.K_DOWN in pressed and pressed[pg.K_DOWN]:
            self.index = (self.index + 1) % len(self.menu_options)
        elif pg.K_UP in pressed and pressed[pg.K_UP]:
            self.index = (self.index - 1) % len(self.menu_options)
