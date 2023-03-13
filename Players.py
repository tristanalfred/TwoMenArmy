import os
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 5
        self.image = None
        self.rect = None

    def move_right(self):
        self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def move_up(self):
        self.rect.y -= self.velocity

    def move_down(self):
        self.rect.y += self.velocity


class Father(Player):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(os.getcwd(), "assets", "father.jpg"))
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 400


class Son(Player):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(os.getcwd(), "assets", "son.jpg"))
        self.rect = self.image.get_rect()

