import datetime

from animation import AnimateSprite

from Projectile import Projectile
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
        pg.draw.rect(surface, max_bar_color, max_bar_position)
        pg.draw.rect(surface, bar_color, bar_position)

    def damage_incured(self, amount):
        self.health -= amount


class Player(Alive):
    def __init__(self, game, entity_name, x, y):
        super().__init__(game, "character", entity_name)
        self.game = game
        self.weight = 10
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 5
        self.rect = pg.Rect(x, y, CHARACTER_SIZE, CHARACTER_SIZE)
        self.all_projectiles = pg.sprite.Group()
        self.direction = RIGHT
        self.controls = {TOP: None, DOWN: None, LEFT: None, RIGHT: None, "attack": None}
        self.controls_delay = {"attack": {"min_ms_delay": 200000, "last_use": datetime.datetime.now()}}

    def update(self, pressed):
        self.move(pressed)
        self.launch_projectile(pressed)
        self.activate(pressed)
        self.animate()

    def activate(self, pressed):
        pass

    def move(self, pressed):
        updated_direction = ""

        if pressed.get(self.controls[LEFT]) and self.rect.x > 0:
            updated_direction += LEFT
            self.move_left()
        elif pressed.get(self.controls[RIGHT]) \
                and self.rect.x < self.game.game_mgmt.screen.get_width() - self.rect.width:
            updated_direction += RIGHT
            self.move_right()
        if pressed.get(self.controls[TOP]) and self.rect.y > 0:
            updated_direction += TOP
            self.move_up()
        elif pressed.get(self.controls[DOWN]) \
                and self.rect.y < self.game.game_mgmt.screen.get_height() - self.rect.height:
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

    def launch_projectile(self, pressed):
        if pressed.get(self.controls["attack"]) \
            and (datetime.datetime.now() - self.controls_delay["attack"]["last_use"]).microseconds \
                > self.controls_delay["attack"]["min_ms_delay"]:
            self.all_projectiles.add(Projectile(self, self.game))
            self.controls_delay["attack"]["last_use"] = datetime.datetime.now()


class Father(Player):
    def __init__(self, game, x, y):
        super().__init__(game, FATHER, x, y)
        self.controls = game.game_mgmt.controls_father

    def activate(self, pressed):
        if pressed.get(self.controls["interaction"]):
            for interaction in self.game.all_interactions:
                if interaction.accessible_by_father:
                    interaction.activate()


class Son(Player):
    def __init__(self, game, x, y):
        super().__init__(game, SON, x, y)
        self.weight = 8
        self.controls = game.game_mgmt.controls_son

    def activate(self, pressed):
        if pressed.get(self.controls["interaction"]):
            for interaction in self.game.all_interactions:
                if interaction.accessible_by_son:
                    interaction.activate()
