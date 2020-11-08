# Made with python 3.8

import pygame
import os
import sys
import pickle
import socket

from common.gamestate import GameState
from common import networking
from client import ball
from client import player

os.environ['SDL_VIDEO_CENTERED'] = '1'  # center window on screen

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000

BALL_WIDTH = 20
BALL_HEIGHT = 20
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 10


def flip_coords(x, y):
    """Flips the coordinates, so that they're seen from the other side of table"""

    x = SCREEN_WIDTH - x
    y = SCREEN_HEIGHT - y
    return (x, y)


def redrawGameWindow():
    pygame.display.update()


def main():

    #
    # pre-runloop setup
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tennis game")
    clock = pygame.time.Clock()

    tennis_ball = ball.Ball()
    player_p1 = player.Player(PLAYER_WIDTH, PLAYER_HEIGHT)
    player_p2 = player.Player(PLAYER_WIDTH, PLAYER_HEIGHT)

    court_color = (0, 133, 102)
    court_stripes = (255, 255, 255)

    # Ball speed, remove later
    ball_speed_x = 0
    ball_speed_y = 0
    ball_speed_z = 0

    run = True
    state = GameState()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((networking.HOST, networking.PORT))
    server.sendall(pickle.dumps(state))
    server.settimeout(5)

    while run:
        data = server.recv(networking.MAX_PACKET_SIZE)
        if not data:
            run = False
        state = pickle.loads(data)

        # Update values from game state
        tennis_ball.x, tennis_ball.y, tennis_ball.z = state.ballPos
        ball_speed_x, ball_speed_y, ball_speed_z = state.ballVelocity
        ball_speed_x, ball_speed_y = flip_coords(
            ball_speed_x, ball_speed_y
        )
        player_p2.x, player_p2.y, player_p2.z = state.opponentPos
        player_p2.x, player_p2.y = flip_coords(
            player_p2.x, player_p2.y
        )
        player_p2.yaw = state.opponentRacketYaw

        # Handle movement/collision anc stuff
        clock.tick(27)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Visuals
        window.fill(court_color)
        tennis_ball.draw(window)
        player_p1.draw(window)
        player_p2.draw(window)
        pygame.draw.aaline(
            window, court_stripes, (0, SCREEN_HEIGHT/2), (SCREEN_WIDTH, SCREEN_HEIGHT/2))

        # Mechanics
        # Player moves after mouse
        player_p1.move(*(pygame.mouse.get_pos()))
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

        # yaw racket
        if keys[pygame.K_a]:
            # yaw like this \
            player_p1.yaw = -1

        elif keys[pygame.K_d]:
            # yaw like this /
            player_p1.yaw = 1

        if not(keys[pygame.K_a] or keys[pygame.K_d]):  # reset yaw from \ or / to _
            player_p1.yaw = 0

        # Player hits ball
        if tennis_ball.x <= player_p1.x + player_p1.width and tennis_ball.x >= player_p1.x:
            if tennis_ball.y + tennis_ball.radius <= player_p1.y + player_p1.height\
                    and tennis_ball.y + tennis_ball.radius >= player_p1.y:
                print(tennis_ball.x, tennis_ball.y,
                        player_p1.x, player_p1.y)

        """
        something like:
            if tennis_ball.x is within player's hitbox x-values (x position and width):
                if (ball.y+ball.radius) is within player's hitbox y-values(y position and height/2):
                    ball hits player, direction is shifted ( velocity * (-1)) (and direction changed if yaw etc)
        """

        """
            something like:
            if ball.x >= SCREEN_WIDTH or ball.x <= 0 or ball.y >= SCREEN_HEIGHT or ball.y <= 0:
                doSomethingCoolHere()

        """

        # Update screen
        redrawGameWindow()

        # update state
        state.ballPos = [tennis_ball.x, tennis_ball.y, tennis_ball.z]
        state.ballVelocity = [ball_speed_x, ball_speed_y, ball_speed_z]
        state.ownPos = [player_p1.x, player_p1.y, player_p1.z]
        state.ownRacketYaw = player_p1.yaw

        # send new state to server
        server.sendall(pickle.dumps(state))


    server.close()
    pygame.quit
    sys.exit()
