# Made with python 3.8

import pygame
import os 
import sys
from client import ball
from client import player

os.environ['SDL_VIDEO_CENTERED'] = '1'  # center window on screen

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000

BALL_WIDTH = 20
BALL_HEIGHT = 20
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 10

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tennis game")
clock = pygame.time.Clock()


def redrawGameWindow():
    pygame.display.update()


def main():
    pass

tennis_ball = ball.Ball()
player_p1 = player.Player(PLAYER_WIDTH, PLAYER_HEIGHT)

ball = pygame.Rect(SCREEN_WIDTH/2 - (BALL_WIDTH/2), SCREEN_HEIGHT/2 - (BALL_HEIGHT/2) ,BALL_WIDTH,BALL_HEIGHT)
player = pygame.Rect(SCREEN_WIDTH - (PLAYER_WIDTH/2), (SCREEN_HEIGHT/2) - (PLAYER_HEIGHT/2), PLAYER_WIDTH, PLAYER_HEIGHT)


court_color = (0,133,102)
court_stripes = (255,255,255)

#Ball speed, remove later
# ball_speed_x = 7
# ball_speed_y = 7

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
    window.fill(court_color)
    tennis_ball.draw(window)
    player_p1.draw(window)
    pygame.draw.aaline(window, court_stripes, (0, SCREEN_HEIGHT/2), (SCREEN_WIDTH, SCREEN_HEIGHT/2))

    # Mechanics
    player_p1.move(*(pygame.mouse.get_pos()))   # Player moves after mouse
    # tennis_ball.move_x(ball_speed_x)
    # tennis_ball.move_y(ball_speed_y)

    # Key bindings
    keys = pygame.key.get_pressed()

    # Tilt racket
    if keys[pygame.K_a]:
        # tilt like this \
        player_p1.tilt = -1

    elif keys[pygame.K_d]:
        # tilt like this /
        player_p1.tilt = 1

    if not(keys[pygame.K_a] or keys[pygame.K_d]):  # reset tilt from \ or / to _
        player_p1.tilt = 0
    # Update screen
    redrawGameWindow()
""" main loop end """


if __name__ == "__main__":
    main()
