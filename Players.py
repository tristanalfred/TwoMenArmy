import pygame
from animation import AnimateSprite

from Projectile import Projectile
from global_variables import *
from tools import *


class Alive(AnimateSprite):
    def __init__(self, game, entity_type, entity_name):
        super().__init__(entity_type, entity_name, "move", RIGHT)
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
    def __init__(self, game, entity_name):
        super().__init__(game, "character", entity_name)
        self.game = game
        self.weight = 10
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 5
        self.rect = None
        self.all_projectiles = pygame.sprite.Group()
        self.direction = RIGHT
        self.controls = {TOP: None, DOWN: None, LEFT: None, RIGHT: None, "attack": None}

    def move(self):
        updated_direction = ""

        if self.game.pressed.get(self.controls[LEFT]) and self.rect.x > 0:
            updated_direction += LEFT
            self.move_left()
        elif self.game.pressed.get(self.controls[RIGHT]) and self.rect.x < self.game.screen.get_width() - self.rect.width:
            updated_direction += RIGHT
            self.move_right()
        if self.game.pressed.get(self.controls[TOP]) and self.rect.y > 0:
            updated_direction += TOP
            self.move_up()
        elif self.game.pressed.get(self.controls[DOWN]) and self.rect.y < self.game.screen.get_height() - self.rect.height:
            updated_direction += DOWN
            self.move_down()

        if updated_direction:
            self.direction = updated_direction
            self.action = "move"
        else:
            self.action = "idle"

    def move_right(self):
        self.rect.x += self.velocity
        obj_collided = check_collisions(self, [self.game.all_enemies, self.game.all_obstacles])
        if obj_collided:
            self.rect.right = obj_collided.rect.left

    def move_left(self):
        self.rect.x -= self.velocity
        obj_collided = check_collisions(self, [self.game.all_enemies, self.game.all_obstacles])
        if obj_collided:
            self.rect.left = obj_collided.rect.right

    def move_up(self):
        self.rect.y -= self.velocity
        obj_collided = check_collisions(self, [self.game.all_enemies, self.game.all_obstacles])
        if obj_collided:
            self.rect.top = obj_collided.rect.bottom

    def move_down(self):
        self.rect.y += self.velocity
        obj_collided = check_collisions(self, [self.game.all_enemies, self.game.all_obstacles])
        if obj_collided:
            self.rect.bottom = obj_collided.rect.top

    def launch_projectile(self):
        self.all_projectiles.add(Projectile(self, self.game))


class Father(Player):
    def __init__(self, game):
        super().__init__(game, "father")
        # self.rect = self.image.get_rect()
        self.rect = pygame.Rect(0, 0, CHARACTER_SIZE, CHARACTER_SIZE)
        self.rect.x = 0
        self.rect.y = 400
        self.controls = {TOP: pygame.K_z, DOWN: pygame.K_s, LEFT: pygame.K_q, RIGHT: pygame.K_d,
                         "attack": pygame.K_SPACE}


class Son(Player):
    def __init__(self, game):
        super().__init__(game, "son")
        # self.rect = self.image.get_rect()
        self.rect = pygame.Rect(0, 0, CHARACTER_SIZE, CHARACTER_SIZE)
        self.weight = 8
        self.controls = {TOP: pygame.K_UP, DOWN: pygame.K_DOWN, LEFT: pygame.K_LEFT, RIGHT: pygame.K_RIGHT,
                         "attack": pygame.K_KP0}
