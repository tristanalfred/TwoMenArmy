import pygame as pg

from GameManagement import GameManagement


pg.init()

# Generate the window of our game
pg.display.set_caption("TwoMenArmy")

# Load the game
game = GameManagement()
while game.running:
    game.run()
pg.quit()
