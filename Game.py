import pygame

from Players import Father, Son
from global_variables import *


class Game:
    def __init__(self, screen, background):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()  # FPS management
        self.background = background
        self.father = Father()
        self.son = Son()
        self.pressed = {}

    def handling_events(self):
        for event in pygame.event.get():
            # Close the game
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                # Start of continuous actions (like projectile launch)
                self.pressed[event.key] = True

                # Non continuous actions (like projectile launch)
                if event.key == pygame.K_SPACE:
                    self.father.launch_projectile()
                elif event.key == pygame.K_KP0:
                    self.son.launch_projectile()

            # End of continuous actions
            elif event.type == pygame.KEYUP:
                self.pressed[event.key] = False

    def update(self):
        # Check the Father moves
        if self.pressed.get(pygame.K_q) and self.father.rect.x > 0:
            self.father.move_left()
        elif self.pressed.get(pygame.K_d) and self.father.rect.x < self.screen.get_width() - self.father.rect.width:
            self.father.move_right()
        if self.pressed.get(pygame.K_z) and self.father.rect.y > 0:
            self.father.move_up()
        elif self.pressed.get(pygame.K_s) and self.father.rect.y < self.screen.get_height() - self.father.rect.height:
            self.father.move_down()

        # Check the Father moves
        if self.pressed.get(pygame.K_LEFT) and self.son.rect.x > 0:
            self.son.move_left()
        elif self.pressed.get(pygame.K_RIGHT) and self.son.rect.x < self.screen.get_width() - self.son.rect.width:
            self.son.move_right()
        if self.pressed.get(pygame.K_UP) and self.son.rect.y > 0:
            self.son.move_up()
        elif self.pressed.get(pygame.K_DOWN) and self.son.rect.y < self.screen.get_height() - self.son.rect.height:
            self.son.move_down()

    def display(self):
        # Apply the background
        self.screen.blit(self.background, (0, 0))

        # Apply players images
        self.screen.blit(self.father.image, self.father.rect)
        self.screen.blit(self.son.image, self.son.rect)

        for projectile in self.father.all_projectiles:
            projectile.move()
        self.father.all_projectiles.draw(self.screen)

        for projectile in self.son.all_projectiles:
            projectile.move()
        self.son.all_projectiles.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handling_events()
            self.update()
            if self.running:
                self.display()

            self.clock.tick(FPS)
