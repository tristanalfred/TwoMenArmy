import pygame

from global_variables import *


class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_name, action, direction):
        super().__init__()
        self.sprite_name = sprite_name
        self.action = action
        self.direction = direction
        self.image = pygame.image.load(os.path.join(CURRENT_DIRECTORY, "assets", sprite_name, action, direction,
                                                    f"{sprite_name}_{action}_{direction}_0.png"))
        self.current_image = 0
        self.images = {}

        for sprite_name, animations_sets in allowed_animations.items():
            for action in animations_sets:
                for direction in directions:
                    self.images[f"{sprite_name}_{action}_{direction}"] = \
                        animations.get(f"{sprite_name}_{action}_{direction}")

    def animate(self):
        self.current_image += 1

        if self.current_image >= len(self.images[f"{self.sprite_name}_{self.action}_{self.direction}"]):
            self.current_image = 0

        self.image = self.images[f"{self.sprite_name}_{self.action}_{self.direction}"][self.current_image]


def load_animation_images(sprite_name, action, direction):
    """
    Load the images of an entity only when the first one is created instead of each entity
    """
    images = []
    path = os.path.join(CURRENT_DIRECTORY, "assets", sprite_name, action, direction)

    for num in range(len(os.listdir(path))):
        images.append(pygame.image.load(os.path.join(path, f"{sprite_name}_{action}_{direction}_{num}.png")))

    return images


allowed_animations = {
    "father": ["move"],
    "son": ["move"]
}

directions = [LEFT, LEFT_UP, UP, RIGHT_UP, RIGHT, RIGHT_DOWN, DOWN, LEFT_DOWN]

animations = {}

for sprite_name, animations_sets in allowed_animations.items():
    for action in animations_sets:
        for direction in directions:
            animations[f"{sprite_name}_{action}_{direction}"] = \
                load_animation_images(sprite_name, action, direction)
