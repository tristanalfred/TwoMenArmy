from Players import Father, Son


class Game:
    def __init__(self):
        # Generate players
        self.father = Father()
        self.son = Son()
        self.pressed = {}
