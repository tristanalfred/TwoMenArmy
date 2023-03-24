from global_variables import *
from tools import *


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.rect = None
        self.blocking = True


class Rock(Obstacle):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(CURRENT_DIRECTORY, "assets", "rock.png")),
                                            (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Door(Obstacle):
    def __init__(self, game, x, y, color="yellow"):
        super().__init__()
        self.game = game
        self.closed = True
        self.image = pygame.Surface((50, 120))
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
        self.image = pygame.Surface((50, 50))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect_activation = game.screen, (0, 0, 0), (self.rect.x - 50, self.rect.y - 50, 100, 100)
        self.door = None
        self.min_distance = 200
        self.already_activated = False

    def show_accessible(self):
        draw_borders_rect(self.game, self)
        # display_text_object(self.game, self, "E")

    def activate(self):
        self.door.open()
        self.already_activated = True


class ExitLevel(Obstacle):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.blocking = False
        self.closed = True
        self.image = pygame.Surface((120, 120))
        self.color = (145, 29, 143)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(x, y))

    def opening(self):
        self.closed = False
        self.image.set_alpha(100)  # Add transparency
