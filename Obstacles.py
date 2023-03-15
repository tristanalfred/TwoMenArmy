import pygame

from global_variables import *


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.rect = None


class Rock(Obstacle):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load(os.path.join(CURRENT_DIRECTORY, "assets", "rock.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
