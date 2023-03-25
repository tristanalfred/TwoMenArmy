from states.state import State
from tools import display_text_screen
from states.game import Game


class Title(State):
    def __init__(self, game_mgmt):
        State.__init__(self, game_mgmt)

    # def update(self, delta_time, actions):
    def update(self, pressed):
        if True in pressed.values():
            new_state = Game(self.game_mgmt)
            new_state.enter_state()
            self.game_mgmt.reset_keys()

    def display(self, screen):
        screen.fill((255, 255, 255))
        display_text_screen(self.game_mgmt, r"Welcome in TwoMenArmy (press any key)")
