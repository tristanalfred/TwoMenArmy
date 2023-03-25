class State:
    def __init__(self, game_mgmt):
        self.game_mgmt = game_mgmt
        self.prev_state = None

    # def update(self, delta_time, actions):
    def update(self, pressed):
        pass

    def display(self, surface):
        pass

    def enter_state(self):
        if len(self.game_mgmt.state_stack) > 1:
            self.prev_state = self.game_mgmt.state_stack[-1]
        self.game_mgmt.state_stack.append(self)

    def exit_state(self):
        self.game_mgmt.state_stack.pop()
