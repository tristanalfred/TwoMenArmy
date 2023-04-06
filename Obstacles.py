from global_variables import *
from tools import *


class Obstacle(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.rect = None
        self.blocking = True


class Rock(Obstacle):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.image = pg.transform.scale(pg.image.load(os.path.join(HOME_DIRECTORY, "assets", "rock.png")), (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Door(Obstacle):
    def __init__(self, game, x, y, color="yellow"):
        super().__init__()
        self.game = game
        self.closed = True
        self.image = pg.Surface((40, 120))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(x, y))

    def open(self):
        self.closed = False
        self.image.set_alpha(100)  # Add transparency


class Interaction:
    def __init__(self):
        self.min_distance = None
        self.accessible_by_father = False
        self.accessible_by_son = False


class Levier(Obstacle, Interaction):
    def __init__(self, game, x, y, color="yellow"):
        Obstacle.__init__(self)
        Interaction.__init__(self)
        self.game = game
        self.image = pg.Surface((50, 50))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect_activation = self.game.game_mgmt.screen, (0, 0, 0), (self.rect.x - 50, self.rect.y - 50, 100, 100)
        self.door = None
        self.min_distance = 200
        self.already_activated = False

    def show_accessible(self):
        draw_borders_rect(self.game.game_mgmt, self)
        # display_text_under_object(self.game, self, "E")

    def activate(self):
        self.door.open()
        self.already_activated = True


class ExitLevel(Obstacle):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.blocking = False
        self.closed = True
        self.image = pg.Surface((120, 120))
        self.color = (145, 29, 143)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(x, y))

    def opening(self):
        self.closed = False
        self.image.set_alpha(100)  # Add transparency
