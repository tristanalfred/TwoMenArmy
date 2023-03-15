import pygame

from global_variables import *


class Projectile(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.velocity = 10
        self.image = pygame.image.load(os.path.join(CURRENT_DIRECTORY, "assets", "projectile.png"))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.center[0] - self.rect.center[0]
        self.rect.y = player.rect.center[1] - self.rect.center[1]
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
        if self.rect.x - self.rect.x < 0 or self.rect.x > SCREEN_WIDTH \
                or self.rect.y - self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.remove()

    def remove(self):
        self.player.all_projectiles.remove(self)
