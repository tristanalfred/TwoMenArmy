import pygame as pg

from entities.players import Alive
from global_variables import *


class Enemy(Alive):
    def __init__(self, game, entity_name):
        super().__init__(game, "enemy", entity_name)
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 5
        self.weight = 10
        self.direction = DOWN
        self.image = None
        self.rect = None


class PunchingBall(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, "punching_ball")
        self.image = pg.image.load(os.path.join(HOME_DIRECTORY, "punching_ball.jpg"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
