import pygame

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
        self.image = pygame.image.load(os.path.join(CURRENT_DIRECTORY, "assets", "rock.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Door(Obstacle):
    def __init__(self, game, x, y, color="yellow"):
        super().__init__()
        self.game = game
        self.closed = True
        self.image = pygame.Surface((50, 200))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(x, y))

    def open(self):
        self.closed = False
        self.image.set_alpha(100)  # Add transparency


class Levier(Obstacle):
    def __init__(self, game, x, y, color="yellow"):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((50, 50))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect_activation = game.screen, (0, 0, 0), (self.rect.x - 50, self.rect.y - 50, 100, 100)
        self.door = find_object_group(self.game.all_obstacles, Door, "color", self.color)

        self.is_accessible()  # TODO : call with correct condition. In Game

    def is_accessible(self):
        draw_borders_rect(self.game, self)
        display_text_object(self.game, self, "E")

    def activate(self):
        self.door.open()
