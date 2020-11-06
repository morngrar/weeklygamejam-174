# Made with python 3.8

import pygame
import os 

os.environ['SDL_VIDEO_CENTERED'] = '1'  # center window on screen

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1600

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tennis game")
clock = pygame.time.Clock()


def redrawGameWindow():
    pygame.display.update()


def main():
    pass


""" main loop """
run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False








    # Update screen
    redrawGameWindow()
""" main loop end """


if __name__=="__main__":
    main()

