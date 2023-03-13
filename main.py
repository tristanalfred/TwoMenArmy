import os
import pygame

from Game import Game

# GLOBAL VARIABLES
CURRENT_DIRECTORY = os.getcwd()

pygame.init()

# Define FPS clock
clock = pygame.time.Clock()
FPS = 60

# Generate the window of our game
pygame.display.set_caption("TwoMenArmy")
screen = pygame.display.set_mode((1080, 720))

# Import background
background = pygame.image.load(
    os.path.join(CURRENT_DIRECTORY, "assets", "background.png"))  # os.path.join allow windows and linux paths

# Load the game
game = Game()

running = True

# Loop executed to display a new frame
while running:
    # Apply the background
    screen.blit(background, (0, 0))

    # Apply players images
    screen.blit(game.father.image, game.father.rect)
    screen.blit(game.son.image, game.son.rect)

    # Check the players moves
    # Father
    if game.pressed.get(pygame.K_q) and game.father.rect.x > 0:
        game.father.move_left()
    if game.pressed.get(pygame.K_d) and game.father.rect.x < screen.get_width() - game.father.rect.width:
        game.father.move_right()
    if game.pressed.get(pygame.K_z) and game.father.rect.y > 0:
        game.father.move_up()
    if game.pressed.get(pygame.K_s) and game.father.rect.y < screen.get_height() - game.father.rect.height:
        game.father.move_down()

    # Son
    if game.pressed.get(pygame.K_LEFT) and game.son.rect.x > 0:
        game.son.move_left()
    if game.pressed.get(pygame.K_RIGHT) and game.son.rect.x < screen.get_width() - game.son.rect.width:
        game.son.move_right()
    if game.pressed.get(pygame.K_UP) and game.son.rect.y > 0:
        game.son.move_up()
    if game.pressed.get(pygame.K_DOWN) and game.son.rect.y < screen.get_height() - game.son.rect.height:
        game.son.move_down()

    # Update Screen
    pygame.display.flip()

    # If the player close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

    clock.tick(FPS)

