import pygame

from Projectile import Projectile
from global_variables import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.weight = 10
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 5
        self.image = None
        self.rect = None
        self.all_projectiles = pygame.sprite.Group()
        self.direction = LEFT

    def move_right(self):
        if not self.game.check_collisions(self, self.game.all_enemies):
            self.rect.x += self.velocity
            self.direction = RIGHT

    def move_left(self):
        if not self.game.check_collisions(self, self.game.all_enemies):
            self.rect.x -= self.velocity
            self.direction = LEFT

    def move_up(self):
        if not self.game.check_collisions(self, self.game.all_enemies):
            self.rect.y -= self.velocity
            self.direction = UP

    def move_down(self):
        if not self.game.check_collisions(self, self.game.all_enemies):
            self.rect.y += self.velocity
            self.direction = DOWN

    def launch_projectile(self):
        self.all_projectiles.add(Projectile(self))


class Father(Player):
    def __init__(self, game):
        super().__init__(game)
        self.image = pygame.image.load(os.path.join(CURRENT_DIRECTORY, "assets", "father.jpg"))
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 400


class Son(Player):
    def __init__(self, game):
        super().__init__(game)
        self.image = pygame.image.load(os.path.join(CURRENT_DIRECTORY, "assets", "son.jpg"))
        self.rect = self.image.get_rect()
        self.weight = 8

