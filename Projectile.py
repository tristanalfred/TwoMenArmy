import pygame

from global_variables import *


class Projectile(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.velocity = 10
        self.image = pygame.image.load(os.path.join(os.getcwd(), "assets", "projectile.png"))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.direction = player.direction
        self.player = player

    def move(self):
        if self.direction == LEFT:
            self.rect.x -= self.velocity
        elif self.direction == RIGHT:
            self.rect.x += self.velocity
        elif self.direction == UP:
            self.rect.y -= self.velocity
        elif self.direction == DOWN:
            self.rect.y += self.velocity

        # Delete the projectile if he left the screen
        if self.rect.x - self.rect.x < 0 or self.rect.x > 1080 or self.rect.y - self.rect.y < 0 or self.rect.y > 720:
            self.remove()

    def remove(self):
        self.player.all_projectiles.remove(self)
