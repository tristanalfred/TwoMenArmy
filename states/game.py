import datetime
import importlib

from Enemies import *
from Obstacles import *
from Players import Father, Son
from global_variables import *
from states.pause_menu import PauseMenu
from states.state import State
from tools import *


class Game(State):
    def __init__(self, game_mgmt):
        State.__init__(self, game_mgmt)
        self.game_mgmt = game_mgmt
        self.background = pg.image.load(
            os.path.join(HOME_DIRECTORY, "assets", "background.png"))  # os.path.join allow windows and linux paths
        self.father = None
        self.son = None
        self.all_enemies = pg.sprite.Group()
        self.all_obstacles = pg.sprite.Group()
        self.all_interactions = pg.sprite.Group()
        self.all_particles = []
        self.actual_level = 1
        self.total_levels = 2
        self.level = None
        self.start_time = datetime.datetime.now()
        self.game_ended = False

        self.load_level(self.actual_level)

    def load_level(self, level_nb):
        self.level = importlib.import_module(f"levels.level{level_nb}")
        self.add_level_entities()

    def add_level_entities(self):
        level_map = self.level.map
        for x in range(17):
            for y in range(25):
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
                elif level_map[x][y] == "X":
                    create_entity(self, ExitLevel, y * 40, x * 40, [self.all_obstacles])

        connect_interactions(self.all_interactions, self.all_obstacles)

    def update(self, pressed):
        """
        Update the state of the game and entities (ex : move a player)
        """
        # Open pause menu
        if pg.K_ESCAPE in pressed and pressed[pg.K_ESCAPE]:
            self.game_mgmt.reset_keys()
            new_state = PauseMenu(self.game_mgmt)
            new_state.enter_state()

        # Update characters
        self.father.update(pressed)
        self.son.update(pressed)

        # Update projectiles
        for projectile in self.father.all_projectiles:
            projectile.move()
        for projectile in self.son.all_projectiles:
            projectile.move()

        # Update Enemies
        for enemy in self.all_enemies:
            if enemy.health <= 0:
                self.all_enemies.remove(enemy)

        # Update particles
        for particle in self.all_particles:
            particle.update()

        # Open the exit
        exit_level = find_object_group(self.all_obstacles, ExitLevel)
        if len(self.all_enemies) == 0:
            if exit_level:
                exit_level.opening()

        # Reach next level
        if exit_level and not exit_level.closed and self.father.rect.colliderect(exit_level) \
                and self.son.rect.colliderect(exit_level):
            clean_level(self)
            self.actual_level += 1
            self.load_level(self.actual_level)
            self.start_time = datetime.datetime.now()
        elif not exit_level and len(self.all_enemies) == 0:
            self.game_ended = True

    def display(self, screen):
        """
        Display all the entities on the screen
        """
        screen.blit(self.background, (0, 0))

        self.father.all_projectiles.draw(screen)
        self.son.all_projectiles.draw(screen)

        self.all_obstacles.draw(screen)

        self.all_enemies.draw(screen)
        for enemy in self.all_enemies:
            enemy.update_health_bar(screen)

        # Apply players images
        screen.blit(self.father.image, self.father.rect)
        screen.blit(self.son.image, self.son.rect)

        self.father.update_health_bar(screen)
        self.son.update_health_bar(screen)

        find_closest_interaction(self.all_interactions, self.father)
        find_closest_interaction(self.all_interactions, self.son)

        for particle in self.all_particles:
            pg.draw.circle(screen, particle.color, particle.center, particle.radius, width=particle.width)

        if (datetime.datetime.now() - self.start_time).seconds < 2:
            display_text_screen(self.game_mgmt, self.level.name)
            pass

        if self.game_ended:
            display_text_screen(self.game_mgmt, "You win !")
