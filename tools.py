import pygame


# TODO : replace game where not needed

def find_object_group(group, entity_type, attribute=None, attribute_value=None):
    for obj in group:
        if isinstance(obj, entity_type) and (not attribute or getattr(obj, attribute) == attribute_value):
            return obj


def display_text_object(game, obj, text):
    render = game.textfont.render(text, True, (255, 0, 0))
    game.screen.blit(render, (obj.rect.x + obj.rect.width/2 - render.get_width()/2, obj.rect.y + obj.rect.height))


def draw_borders_rect(game, obj):
    for i in range(4):
        pygame.draw.rect(game.screen, (0, 0, 0),
                         (obj.rect.x - i, obj.rect.y - i, obj.rect.width, obj.rect.height), 1)


def spawn_monster(game, enemy_type, x, y):
    enemy = enemy_type(game, x, y)
    game.all_enemies.add(enemy)


def add_obstacle(game, obstacle_type, x, y):
    obstacle = obstacle_type(game, x, y)
    game.all_obstacles.add(obstacle)


def check_collisions(sprite, groups):
    if not isinstance(groups, list):
        groups = [groups]
    for group in groups:
        for obj in group:
            # if pygame.sprite.collide_mask(sprite, obj):  # For pixel perfect collision
            if sprite.rect.colliderect(obj) \
                    and not (type(obj).__name__ == "Door" and obj.closed is False):  # For image size collision
                return obj
    return False
