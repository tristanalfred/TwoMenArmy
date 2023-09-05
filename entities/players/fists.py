import pygame as pg
from enum import Enum

from global_variables import *


class BackForth(Enum):
    NEUTRAL = "neutral"
    BACK = "back"
    FORTH = "forth"


class Fist(pg.sprite.Sprite):
    def __init__(self, player, color="red"):
        super().__init__()
        self.player = player
        self.image = pg.Surface((20, 20))
        self.color = color
        self.image.fill(self.color)
        self.relative_rect = self.image.get_rect(center=self.player.rect.topright)
        self.rect = self.image.get_rect(center=self.player.rect.topright)

        self.max_range = 75
        self.distance_character = 0
        self.velocity = 15
        self.backforth = BackForth.NEUTRAL

    def update(self):
        self.update_relative_position()
        self.update_true_position()

    def update_relative_position(self):
        """
        Because we are linked to the player, we use this method to link the fist to the player, but it doesn't always
        represent the true position of the fist
        """
        pass

    def update_true_position(self):
        """
        True position of the fist, calculated with relative position and variables
        """
        if self.backforth == BackForth.NEUTRAL:
            self.rect = self.relative_rect
            return

        # Update distance
        elif self.backforth == BackForth.FORTH:
            self.distance_character += self.velocity
        else:
            self.distance_character -= self.velocity

        # Avoid unusual distances
        if self.distance_character > self.max_range:
            self.distance_character = self.max_range
            self.backforth = BackForth.BACK
        elif self.distance_character <= 0 and self.backforth == BackForth.BACK:
            self.distance_character = 0
            self.backforth = BackForth.NEUTRAL

        # Default value
        self.rect.x = self.relative_rect.x
        self.rect.y = self.relative_rect.y

        # Use relative position and distance of the character to get the true position
        if LEFT in self.player.direction:
            self.rect.x = self.relative_rect.x - self.distance_character
        elif RIGHT in self.player.direction:
            self.rect.x = self.relative_rect.x + self.distance_character
        if TOP in self.player.direction:
            self.rect.y = self.relative_rect.y - self.distance_character
        elif DOWN in self.player.direction:
            self.rect.y = self.relative_rect.y + self.distance_character


class RightFist(Fist):
    def __init__(self, player, color="red"):
        super().__init__(player, color)

    def update_relative_position(self):
        """
        Note for later : We should probably have player's attributes for each relative directions,
                         so we only have one line :  self.relative_rect.center = self.player.relative_rect.top_right
        """
        if self.player.direction == TOP:
            self.relative_rect.center = self.player.rect.topright
        elif self.player.direction == DOWN:
            self.relative_rect.center = self.player.rect.bottomleft
        elif self.player.direction == LEFT:
            self.relative_rect.center = self.player.rect.topleft
        elif self.player.direction == RIGHT:
            self.relative_rect.center = self.player.rect.bottomright

        elif self.player.direction == LEFT_TOP:
            self.relative_rect.center = self.player.rect.midtop
        elif self.player.direction == RIGHT_TOP:
            self.relative_rect.center = self.player.rect.midright
        elif self.player.direction == LEFT_BOTTOM:
            self.relative_rect.center = self.player.rect.midleft
        elif self.player.direction == RIGHT_BOTTOM:
            self.relative_rect.center = self.player.rect.midbottom


class LeftFist(Fist):
    def __init__(self, player, color="orange"):
        super().__init__(player, color)

    def update_relative_position(self):
        if self.player.direction == TOP:
            self.relative_rect.center = self.player.rect.topleft
        elif self.player.direction == DOWN:
            self.relative_rect.center = self.player.rect.bottomright
        elif self.player.direction == LEFT:
            self.relative_rect.center = self.player.rect.bottomleft
        elif self.player.direction == RIGHT:
            self.relative_rect.center = self.player.rect.topright

        elif self.player.direction == LEFT_TOP:
            self.relative_rect.center = self.player.rect.midleft
        elif self.player.direction == RIGHT_TOP:
            self.relative_rect.center = self.player.rect.midtop
        elif self.player.direction == LEFT_BOTTOM:
            self.relative_rect.center = self.player.rect.midbottom
        elif self.player.direction == RIGHT_BOTTOM:
            self.relative_rect.center = self.player.rect.midright

