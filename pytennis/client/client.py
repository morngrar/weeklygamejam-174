# Made with python 3.8

import pygame
import os 
import sys
import pickle

from common.gamestate import GameState
from client import ball
from client import player

os.environ['SDL_VIDEO_CENTERED'] = '1'  # center window on screen

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000

BALL_WIDTH = 20
BALL_HEIGHT = 20
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 10



def redrawGameWindow():
    pygame.display.update()


def main():

    #
    ## pre-runloop setup
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tennis game")
    clock = pygame.time.Clock()

    tennis_ball = ball.Ball()
    player_p1 = player.Player(PLAYER_WIDTH, PLAYER_HEIGHT)

    ball = pygame.Rect(SCREEN_WIDTH/2 - (BALL_WIDTH/2), SCREEN_HEIGHT/2 - (BALL_HEIGHT/2) ,BALL_WIDTH,BALL_HEIGHT)
    player = pygame.Rect(SCREEN_WIDTH - (PLAYER_WIDTH/2), (SCREEN_HEIGHT/2) - (PLAYER_HEIGHT/2), PLAYER_WIDTH, PLAYER_HEIGHT)


    court_color = (0,133,102)
    court_stripes = (255,255,255)

    #Ball speed, remove later
    ball_speed_x = 0
    ball_speed_y = 0

    run = True

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.connect((networking.HOST, networking.PORT))
        server.sendall(pickle.dumps(state))

        while run:
            data = server.recv(networking.MAX_PACKET_SIZE)
            if not data:
                run = False
            state = pickle.loads(data)


            # Handle movement/collision anc stuff
            clock.tick(27)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Visuals
            window.fill(court_color)
            tennis_ball.draw(window)
            player_p1.draw(window)
            pygame.draw.aaline(window, court_stripes, (0, SCREEN_HEIGHT/2), (SCREEN_WIDTH, SCREEN_HEIGHT/2))

            # Mechanics
            player_p1.move(*(pygame.mouse.get_pos()))   # Player moves after mouse
            tennis_ball.move_x(ball_speed_x)
            tennis_ball.move_y(ball_speed_y)
            
            # Ball wall collision
            if tennis_ball.x >= SCREEN_WIDTH + tennis_ball.radius or tennis_ball.x <= 0 + tennis_ball.radius:
                ball_speed_x *= -1
                tennis_ball.move_x(ball_speed_x)
            
            if tennis_ball.y >= SCREEN_HEIGHT + tennis_ball.radius or tennis_ball.y <= 0 + tennis_ball.radius:
                ball_speed_y *= -1
                tennis_ball.move_y(ball_speed_y)



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
            

            # Player hits ball
            if tennis_ball.x <= player_p1.x + player_p1.width and tennis_ball.x >= player_p1.x:
                if tennis_ball.y + tennis_ball.radius <= player_p1.y + player_p1.height\
                    and tennis_ball.y + tennis_ball.radius >= player_p1.y:
                    print(tennis_ball.x , tennis_ball.y, player_p1.x, player_p1.y)

            """
            something like:
                if tennis_ball.x is within player's hitbox x-values (x position and width):
                    if (ball.y+ball.radius) is within player's hitbox y-values(y position and height/2):
                        ball hits player, direction is shifted ( velocity * (-1)) (and direction changed if tilted etc)
            """

            """
                something like:
                if ball.x >= SCREEN_WIDTH or ball.x <= 0 or ball.y >= SCREEN_HEIGHT or ball.y <= 0:
                    doSomethingCoolHere()

            """

            # Update screen
            redrawGameWindow()

            # send new state to server
            server.sendall(pickle.dumps(state))


    pygame.quit
    sys.exit()

