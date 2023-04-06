import pygame as pg

from global_variables import *


class AnimateSprite(pg.sprite.Sprite):
    def __init__(self, entity_type, sprite_name, action, direction):
        super().__init__()
        self.entity_type = entity_type
        self.sprite_name = sprite_name
        self.action = action
        self.direction = direction
        # self.image = pg.image.load(os.path.join(HOME_DIRECTORY, "assets", entity_type, sprite_name, update_actions,
        #                                             direction, f"{sprite_name}_{update_actions}_{direction}_0.png"))
        self.image = pg.transform.scale(
            pg.image.load(os.path.join(HOME_DIRECTORY, "assets", entity_type, sprite_name, action, direction,
                                           f"{sprite_name}_{action}_{direction}_0.png")), (500, 500))
        self.current_image = 0
        self.images = {}

        for entity_type, sprite in allowed_animations.items():
            for sprite_name, animations_sets in sprite.items():
                for action in animations_sets:
                    for direction in directions:
                        self.images[f"{sprite_name}_{action}_{direction}"] = \
                            animations.get(f"{sprite_name}_{action}_{direction}")

    def animate(self):
        self.current_image += 1

        if self.current_image >= len(self.images[f"{self.sprite_name}_{self.action}_{self.direction}"]):
            self.current_image = 0

        self.image = self.images[f"{self.sprite_name}_{self.action}_{self.direction}"][self.current_image]


def load_animation_images(entity_type, sprite_name, action, direction):
    """
    Load the images of an entity only when the first one is created instead of each entity
    """
    images = []
    path = os.path.join(HOME_DIRECTORY, "assets", entity_type, sprite_name, action, direction)

    for num in range(len(os.listdir(path))):
        images.append(pg.transform.scale(pg.image.load(
            os.path.join(path, f"{sprite_name}_{action}_{direction}_{num}.png")), (CHARACTER_SIZE, CHARACTER_SIZE)))

    return images


allowed_animations = {
    "character": {
        FATHER: ["idle", "move"],
        SON: ["idle", "move"]
    }
}

directions = [LEFT, LEFT_TOP, TOP, RIGHT_TOP, RIGHT, RIGHTBOTTOM, DOWN, LEFT_BOTTOM]

animations = {}

for entity_type, sprite in allowed_animations.items():
    for sprite_name, animations_sets in sprite.items():
        for action in animations_sets:
            for direction in directions:
                animations[f"{sprite_name}_{action}_{direction}"] = \
                    load_animation_images(entity_type, sprite_name, action, direction)