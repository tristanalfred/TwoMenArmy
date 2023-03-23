import pygame

from Game import Game
from global_variables import *


pygame.init()

# Generate the window of our game
pygame.display.set_caption("TwoMenArmy")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

background = pygame.image.load(
            os.path.join(CURRENT_DIRECTORY, "assets", "background.png"))  # os.path.join allow windows and linux paths

text_font = pygame.font.SysFont("Arial", 36)

# Load the game
game = Game(screen, background, text_font)
game.run()
pygame.quit()
