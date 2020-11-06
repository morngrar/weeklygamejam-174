# Made with python 3.8

import pygame, sys
from client import ball

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
BALL_WIDTH = 20
BALL_HEIGHT = 20
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tennis game")
clock = pygame.time.Clock()


def redrawGameWindow():
    pygame.display.update()

def main():
    pass

tennis_ball = ball.Ball()

ball = pygame.Rect(SCREEN_WIDTH/2 - (BALL_WIDTH/2), SCREEN_HEIGHT/2 - (BALL_HEIGHT/2) ,BALL_WIDTH,BALL_HEIGHT)
player = pygame.Rect(SCREEN_WIDTH - (PLAYER_WIDTH/2), (SCREEN_HEIGHT/2) - (PLAYER_HEIGHT/2), PLAYER_WIDTH, PLAYER_HEIGHT)


court_color = (0,133,102)

""" main loop """
run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit
            sys.exit()

    # Visuals
    tennis_ball.draw()

    
    # Update screen
    redrawGameWindow()
""" main loop end """


if __name__=="__main__":
    main()

