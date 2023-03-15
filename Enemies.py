import pygame

from global_variables import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 5
        self.weight = 10
        self.direction = DOWN
        self.image = None
        self.rect = None


class PunchingBall(Enemy):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join(CURRENT_DIRECTORY, "assets", "father.jpg"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
