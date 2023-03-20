import pygame
import sys

from Enemies import PunchingBall
from Obstacles import Door, Rock, Levier
from Players import Father, Son
from global_variables import *


class Game:
    def __init__(self, screen, background):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()  # FPS management
        self.background = background
        self.father = Father(self)
        self.son = Son(self)
        self.all_enemies = pygame.sprite.Group()
        self.all_obstacles = pygame.sprite.Group()
        self.pressed = {}

        self.spawn_monster(PunchingBall, SCREEN_WIDTH/2, 100)
        self.add_obstacle(Rock, 400, 0)
        self.add_obstacle(Rock, 400, 70)
        self.add_obstacle(Rock, 400, 140)
        self.add_obstacle(Rock, 400, 210)
        self.add_obstacle(Rock, 400, 280)
        self.add_obstacle(Door, 400, 350)
        self.add_obstacle(Levier, 200, 450)

    def spawn_monster(self, enemy_type, x, y):
        enemy = enemy_type(self, x, y)
        self.all_enemies.add(enemy)

    def add_obstacle(self, obstacle_type, x, y):
        obstacle = obstacle_type(self, x, y)
        self.all_obstacles.add(obstacle)

    def check_collisions(self, sprite, groups):
        if not isinstance(groups, list):
            groups = [groups]
        for group in groups:
            for obj in group:
                if pygame.sprite.collide_mask(sprite, obj):
                    return obj
        return False

    def handling_events(self):
        """
        Get all the events (ex : key pressed)
        """
        for event in pygame.event.get():
            # Close the game
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                # Start of continuous actions (ex : move)
                self.pressed[event.key] = True

                # Non continuous actions (ex : projectile launch)
                if event.key == pygame.K_SPACE:
                    self.father.launch_projectile()
                elif event.key == pygame.K_KP0:
                    self.son.launch_projectile()

            # End of continuous actions
            elif event.type == pygame.KEYUP:
                self.pressed[event.key] = False

    def update(self):
        """
        Update the state of the game and entities (ex : move a player)
        """
        self.father.move()
        self.son.move()

        self.father.animate()
        self.son.animate()

        for projectile in self.father.all_projectiles:
            projectile.move()

        for projectile in self.son.all_projectiles:
            projectile.move()

        for enemy in self.all_enemies:
            if enemy.health <= 0:
                self.all_enemies.remove(enemy)

    def display(self):
        """
        Display all the entities on the screen
        """
        # Apply the background
        self.screen.blit(self.background, (0, 0))

        self.father.all_projectiles.draw(self.screen)
        self.son.all_projectiles.draw(self.screen)

        self.all_obstacles.draw(self.screen)

        self.all_enemies.draw(self.screen)
        for enemy in self.all_enemies:
            enemy.update_health_bar(self.screen)

        # Apply players images
        self.screen.blit(self.father.image, self.father.rect)
        self.screen.blit(self.son.image, self.son.rect)

        self.father.update_health_bar(self.screen)
        self.son.update_health_bar(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.clock.tick(FPS)
