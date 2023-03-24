import sys

from Enemies import PunchingBall
from Obstacles import Door, Rock, Levier
from Players import Father, Son
from global_variables import *
from levels import level1, level2
from tools import *


class Game:
    def __init__(self, screen, background, text_font):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()  # FPS management
        self.background = background
        self.father = None
        self.son = None
        self.all_enemies = pygame.sprite.Group()
        self.all_obstacles = pygame.sprite.Group()
        self.all_interactions = pygame.sprite.Group()
        self.pressed = {}
        self.text_font = text_font
        self.actual_level = 1

        self.load_level(self.actual_level)

    def load_level(self, level):
        level_map = None
        if level == 1:
            level_map = level1.map
        elif level == 2:
            level_map = level2.map

        self.add_level_entities(level_map)

    def add_level_entities(self, level_map):
        for x in range(17):
            for y in range(26):
                if level_map[x][y] == "F":
                    self.father = Father(self, y*40, x*40)
                elif level_map[x][y] == "S":
                    self.son = Son(self, y*40, x*40)
                elif level_map[x][y] == "R":
                    create_entity(self, Rock, y*40, x*40, [self.all_obstacles])
                elif level_map[x][y] == "D":
                    create_entity(self, Door, y*40, x*40, [self.all_obstacles])
                elif level_map[x][y] == "L":
                    create_entity(self, Levier, y*40, x*40, [self.all_obstacles, self.all_interactions])
                elif level_map[x][y] == "E-PB":
                    create_entity(self, PunchingBall, y*40, x*40, [self.all_enemies])

        connect_interactions(self.all_interactions, self.all_obstacles)

    def handling_events(self):
        """
        Get all the events, like key pressed
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
                if event.key == pygame.K_KP0:
                    self.son.launch_projectile()
                if event.key == pygame.K_e:
                    for interaction in self.all_interactions:
                        if interaction.accessible_by_father:
                            interaction.activate()
                if event.key == pygame.K_KP1:
                    for interaction in self.all_interactions:
                        if interaction.accessible_by_son:
                            interaction.activate()

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

        # Reach next level if all the enemies are dead
        if len(self.all_enemies) == 0:
            clean_level(self)
            self.actual_level += 1
            self.load_level(self.actual_level)

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

        find_closest_interaction(self.all_interactions, self.father)
        find_closest_interaction(self.all_interactions, self.son)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.clock.tick(FPS)
