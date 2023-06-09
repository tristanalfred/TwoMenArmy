import pygame

from global_variables import *


class Projectile(pygame.sprite.Sprite):
    def __init__(self, player, game):
        super().__init__()
        self.game = game
        self.velocity = 10
        self.damage = 10
        self.image = pygame.image.load(os.path.join(CURRENT_DIRECTORY, "assets", "projectile.png"))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.center[0] - self.rect.center[0]
        self.rect.y = player.rect.center[1] - self.rect.center[1]
        self.direction = player.direction
        self.player = player

    def move(self):
        if LEFT in self.direction:
            self.rect.x -= self.velocity
        elif RIGHT in self.direction:
            self.rect.x += self.velocity
        if TOP in self.direction:
            self.rect.y -= self.velocity
        elif DOWN in self.direction:
            self.rect.y += self.velocity

        # Destroys the projectile on impact, and inflicts damage if it's an enemy
        obj_collided = self.game.check_collisions(self, [self.game.all_enemies, self.game.all_obstacles])
        if obj_collided:
            if obj_collided not in self.game.all_obstacles:
                obj_collided.damage_incured(self.player.attack)
            self.remove()

        # Delete the projectile if he left the screen
        if self.rect.x - self.rect.x < 0 or self.rect.x > SCREEN_WIDTH \
                or self.rect.y - self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.remove()

    def remove(self):
        self.player.all_projectiles.remove(self)
