import pygame

from global_variables import *


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
    def __init__(self, game, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 200))
        self.image.fill('yellow')
        self.rect = self.image.get_rect(topleft=(x, y))

    def opening(self):
        self.blocking = False
        self.image.fill('red')


class Levier(Obstacle):
    def __init__(self, game, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill('yellow')
        self.rect = self.image.get_rect(topleft=(x, y))


