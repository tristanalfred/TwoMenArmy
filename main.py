import pygame


pygame.init()


# Generate the window of our game
pygame.display.set_caption("TwoMenArmy")
pygame.display.set_mode((1080, 720))

running = True

# Loop executed to display a new frame
while running:
    # If the player close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
