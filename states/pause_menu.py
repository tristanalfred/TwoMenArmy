import json

import pygame as pg

from global_variables import *
from states.state import State
from states.controls_menu import ControlsMenu
from tools import *


class PauseMenu(State):
    def __init__(self, game_mgmt):
        State.__init__(self, game_mgmt)
        self.game_mgmt = game_mgmt
        # Set the menu
        self.menu_img = pg.image.load(os.path.join(CURRENT_DIRECTORY, "assets", "menu", "menu.png"))
        self.menu_rect = self.menu_img.get_rect()
        self.menu_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        # Set the cursor and menu states
        self.menu_options = {0: "Party", 1: "Items", 2: "Magic", 3: "Exit"}
        self.index = 0
        self.cursor_img = pg.image.load(os.path.join(CURRENT_DIRECTORY, "assets", "menu", "cursor.png"))
        self.cursor_rect = self.cursor_img.get_rect()
        self.cursor_pos_y = self.menu_rect.y + 38
        self.cursor_rect.x, self.cursor_rect.y = self.menu_rect.x + 10, self.cursor_pos_y

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
        screen.blit(self.menu_img, self.menu_rect)
        screen.blit(self.cursor_img, self.cursor_rect)

    def transition_state(self):
        if self.menu_options[self.index] == "Party":
            new_state = ControlsMenu(self.game_mgmt)
            new_state.enter_state()
        elif self.menu_options[self.index] == "Items":
            pass  # TO-DO
        elif self.menu_options[self.index] == "Magic":
            pass  # TO-DO
        elif self.menu_options[self.index] == "Exit":
            while len(self.game_mgmt.state_stack) > 1:
                self.game_mgmt.state_stack.pop()

    def update_cursor(self, pressed):
        if pg.K_DOWN in pressed and pressed[pg.K_DOWN]:
            self.index = (self.index + 1) % len(self.menu_options)
        elif pg.K_UP in pressed and pressed[pg.K_UP]:
            self.index = (self.index - 1) % len(self.menu_options)
        self.cursor_rect.y = self.cursor_pos_y + (self.index * 32)
