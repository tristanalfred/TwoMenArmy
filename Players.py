import pygame

from Projectile import Projectile
from global_variables import *


class Alive(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.rect = None
        self.health = 10
        self.max_health = 10

    def update_health_bar(self, surface):
        bar_color = (111, 210, 46)  # Color of health bar
        max_bar_color = (50, 50, 50)
        bar_position = [self.rect.center[0] - SIZE_HEALTH_BAR/2, self.rect.y + (self.rect.bottom - self.rect.top),
                        SIZE_HEALTH_BAR * (self.health / self.max_health), 5]
        max_bar_position = [self.rect.center[0] - SIZE_HEALTH_BAR/2, self.rect.y + (self.rect.bottom - self.rect.top), SIZE_HEALTH_BAR, 5]

        # Draw bar
        pygame.draw.rect(surface, max_bar_color, max_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)

    def damage_incured(self, amount):
        self.health -= amount


class Player(Alive):
    def __init__(self, game):
        super().__init__(game)
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
        self.direction = RIGHT
        self.rect.x += self.velocity
        obj_collided = self.game.check_collisions(self, [self.game.all_enemies, self.game.all_obstacles])
        if obj_collided:
            self.rect.right = obj_collided.rect.left

    def move_left(self):
        self.direction = LEFT
        self.rect.x -= self.velocity
        obj_collided = self.game.check_collisions(self, [self.game.all_enemies, self.game.all_obstacles])
        if obj_collided:
            self.rect.left = obj_collided.rect.right

    def move_up(self):
        self.direction = UP
        self.rect.y -= self.velocity
        obj_collided = self.game.check_collisions(self, [self.game.all_enemies, self.game.all_obstacles])
        if obj_collided:
            self.rect.top = obj_collided.rect.bottom

    def move_down(self):
        self.direction = DOWN
        self.rect.y += self.velocity
        obj_collided = self.game.check_collisions(self, [self.game.all_enemies, self.game.all_obstacles])
        if obj_collided:
            self.rect.bottom = obj_collided.rect.top

    def launch_projectile(self):
        self.all_projectiles.add(Projectile(self, self.game))


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

