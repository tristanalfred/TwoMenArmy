import pygame
from math import sqrt


# TODO : replace game where not needed


def find_closest_interaction(all_interactions, player):
    closest_interaction_accessible = None
    distance_interaction = {}

    for interaction in all_interactions:
        if sqrt((player.rect.center[0] - interaction.rect.center[0]) ** 2 +
                (player.rect.center[1] - interaction.rect.center[1]) ** 2) \
                < interaction.min_distance\
                and (type(interaction).__name__ != "Levier" or not interaction.already_activated):
            distance_interaction[interaction] = interaction.min_distance

    if distance_interaction:
        closest_interaction_accessible = min(distance_interaction, key=distance_interaction.get)
        if type(player).__name__ == "Father":
            closest_interaction_accessible.accessible_by_father = True
        else:
            closest_interaction_accessible.accessible_by_son = True
        closest_interaction_accessible.show_accessible()

    for interaction in all_interactions:
        if interaction and interaction != closest_interaction_accessible:
            if type(player).__name__ == "Father":
                interaction.accessible_by_father = False
            else:
                interaction.accessible_by_son = False


def find_object_group(group, entity_type, attribute=None, attribute_value=None):
    for obj in group:
        if isinstance(obj, entity_type) and (not attribute or getattr(obj, attribute) == attribute_value):
            return obj


def display_text_object(game, obj, text):
    render = game.text_font.render(text, True, (255, 0, 0))
    game.screen.blit(render, (obj.rect.x + obj.rect.width/2 - render.get_width()/2, obj.rect.y + obj.rect.height))


def draw_borders_rect(game, obj):
    for i in range(4):
        pygame.draw.rect(game.screen, (0, 0, 0),
                         (obj.rect.x - i, obj.rect.y - i, obj.rect.width, obj.rect.height), 1)


def create_entity(game, entity_type, x, y, groups=None):
    entity = entity_type(game, x, y)

    if groups:
        for group in groups:
            group.add(entity)


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
