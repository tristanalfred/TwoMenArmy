import pygame as pg
from math import sqrt

from global_variables import *


# TODO : replace game where not needed


def connect_interactions(all_interactions, all_obstacles):
    for interaction in all_interactions:
        if type(interaction).__name__ == "Levier":
            interaction.door = find_object_group(all_obstacles, "Door", "color", interaction.color)


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
    if not isinstance(entity_type, str):
        entity_type = entity_type.__name__

    for obj in group:
        if type(obj).__name__ == entity_type and (not attribute or getattr(obj, attribute) == attribute_value):
            return obj


def display_text_under_object(game_mgmt, obj, text):
    render = game_mgmt.text_font_object.render(text, True, (255, 0, 0))
    game_mgmt.screen.blit(render, (obj.rect.x + obj.rect.width/2 - render.get_width()/2, obj.rect.y + obj.rect.height))


def display_text_middle_rect(game_mgmt, rect, text):
    render = game_mgmt.text_font_object.render(text, True, (0, 0, 0))
    game_mgmt.screen.blit(render, (rect.x + rect.width/2 - render.get_width()/2,
                                   rect.y + rect.height/2 - render.get_height()/2))


def display_text_screen(game_mgmt, text):
    render = game_mgmt.text_font_screen.render(text, True, (50, 50, 50))
    game_mgmt.screen.blit(render, (game_mgmt.screen.get_size()[0]/2 - render.get_width()/2,
                                   game_mgmt.screen.get_size()[1]/2 - render.get_height()/2))


def display_grey_filter(screen):
    grey_filter_img = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    grey_filter_img.fill("black")
    grey_filter_img.set_alpha(100)
    screen.blit(grey_filter_img, grey_filter_img.get_rect(topleft=(0, 0)))


def draw_borders_rect(game_mgmt, obj):
    for i in range(4):
        pg.draw.rect(game_mgmt.screen, (0, 0, 0),
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
            if sprite.rect.colliderect(obj) \
                    and not ((type(obj).__name__ == "Door" or (type(obj).__name__ == "ExitLevel"))
                             and obj.closed is False):
                return obj
    return False


def clean_level(game):
    game.all_obstacles.empty()
    game.all_interactions.empty()
    game.all_enemies.empty()
