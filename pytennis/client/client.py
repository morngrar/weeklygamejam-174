# Made with python 3.8

import pygame
from pygame.math import Vector2
import os
import sys
import pickle
import socket

from common.gamestate import GameState
from common import networking
from client import ball
from client import player
from client.statusbar import Statusbar

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'  # center window on screen

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1310

BALL_WIDTH = 20
BALL_HEIGHT = 20
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 10

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()




def flip_coords(v):
    """Flips the coordinates, so that they're seen from the other side of table"""

    vector = Vector2(v)
    vector.x = SCREEN_WIDTH - vector.x
    vector.y = SCREEN_HEIGHT - vector.y
    return vector

image_background_original = pygame.image.load(os.path.join('resources', 'pytennis_court.png'))
image_background = pygame.transform.scale(image_background_original, (SCREEN_WIDTH, SCREEN_HEIGHT-30))


def dist(line, x3, y3):
    """Returns shortest distance from line to point"""
    x1, y1, x2, y2 = line
    px = x2-x1
    py = y2-y1
    norm = px*px + py*py
    if norm == 0:
        return None
    u = ((x3 - x1) * px + (y3 - y1) * py) / float(norm)
    if u > 1:
        u = 1
    elif u < 0:
        u = 0
    x = x1 + u * px
    y = y1 + u * py
    dx = x - x3
    dy = y - y3
    dist = (dx*dx + dy*dy)**.5

    return dist


def main():

    #
    # pre-runloop setup
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tennis game")
    clock = pygame.time.Clock()

    def p1_serve():
        tennis_ball.pos.x = SCREEN_WIDTH / 2
        tennis_ball.pos.y = SCREEN_HEIGHT*0.75
        ball_velocity = Vector2(0, 0)

    def p2_serve():
        tennis_ball.pos.x = SCREEN_WIDTH / 2
        tennis_ball.pos.y = SCREEN_HEIGHT*0.25
        ball_velocity = Vector2(0, 0)

    tennis_ball = ball.Ball()
    player_p1 = player.Player(PLAYER_WIDTH, PLAYER_HEIGHT)
    player_p2 = player.Player(PLAYER_WIDTH, PLAYER_HEIGHT)
    player_p2.yaw_angle *= -1
    statusbar = Statusbar(SCREEN_WIDTH, 30)

    court_color = (0, 133, 102)
    court_stripes = (255, 255, 255)

    ball_velocity = Vector2()

    BALL_FRICTION_FACTOR = 0.2
    BALL_MAX_SPEED = 40

    YAW_VELOCITY = Vector2(0, -1)
    YAW_ANGLING = Vector2(-1, 0)   # positive when /
    YAW_ACCEL = 30

    pygame.mouse.set_visible(False)

    p1_serve()

    run = True
    i = 0

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((networking.HOST, networking.PORT))

    handshake = server.recv(networking.MAX_PACKET_SIZE)
    if not handshake or handshake != networking.CONNECTED_MSG:
        logger.info("Failed to acquire handshake: %s", handshake)
        run = False
    else:
        logger.info("Connected with opponent")
        server.settimeout(5)

    
    while run:
        clock.tick(100)     # refresh rate
        i += 1              # counter for paddle velocity


        # handle x-button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        data = server.recv(networking.MAX_PACKET_SIZE)
        if not data:
            run = False
        state = pickle.loads(data)

        # Update values from game state
        tennis_ball.pos = state.ballPos
        tennis_ball.pos = flip_coords(tennis_ball.pos)
        ball_velocity = state.ballVelocity
        ball_velocity = -(ball_velocity)

        player_p2.pos = state.opponentPos
        player_p2.pos = flip_coords(player_p2.pos)
        player_p2.pos.x -= player_p2.width
        player_p2.pos.y -= player_p2.height
        player_p2.yaw = state.opponentRacketYaw
        player_p2.yaw *= -1

        # Handle movement/collision and stuff

        ###########################################################
        # Ball wall collision -- remove when ready for multiplayer
        ###########################################################
        if (
            tennis_ball.pos.x + tennis_ball.radius >= SCREEN_WIDTH 
            or tennis_ball.pos.x <= 0 + tennis_ball.radius
        ):
            tennis_ball.pos.x = SCREEN_WIDTH / 2
            tennis_ball.pos.y = SCREEN_HEIGHT*0.75
            ball_velocity = Vector2(0, 0)

        if tennis_ball.pos.y <= 0 + tennis_ball.radius:
            ball_velocity = -(ball_velocity)

        if tennis_ball.pos.y >= SCREEN_HEIGHT:
            tennis_ball.pos.y = SCREEN_HEIGHT*0.75
            ball_velocity = Vector2(0, 0)
        ##########################################################s


        # find and draw collision line on player 1
        line = player_p1.get_center_line()
        start = (line[0], line[1])
        end = (line[2], line[3])
        pygame.draw.line(window, (200, 200, 0), start, end)

        distance_to_ball = dist(line, tennis_ball.pos.x, tennis_ball.pos.y)

        # If the ball is on player's side            # and distance is small enough to ball
        if tennis_ball.pos.y >= SCREEN_HEIGHT/2 and distance_to_ball <= tennis_ball.radius:
            if ball_velocity.y >= 0:
                logger.debug("Collision")
                ball_velocity = Vector2(player_p1.vel) - ball_velocity 

                # adds a vector force for paddle yaw
                ball_velocity += (YAW_VELOCITY + YAW_ANGLING * player_p1.yaw) * YAW_ACCEL 

                # decelerate (slows down ball if paddle is still)
                ball_velocity *= 0.6

                # if speed isn't limited, paddle can clip through ball
                while ball_velocity.magnitude() > BALL_MAX_SPEED:       
                    ball_velocity *= 0.9

        player_p1.move(*(pygame.mouse.get_pos()))   # Paddle moves after mouse

        if i > 5:   # for velocity to not be 0, only sample intermittently
            player_p1.last_pos = Vector2(player_p1.pos)
            i = 0
        player_p1.vel = (player_p1.pos - player_p1.last_pos)*2

        tennis_ball.pos += ball_velocity * BALL_FRICTION_FACTOR

        logger.debug("Ball velocity: %s", ball_velocity)
        logger.debug("Player velocity: %s", player_p1.vel)


        # # Player can't move to other side of court or "out of window"
        # if player_p1.pos.x >= SCREEN_WIDTH - (player_p1.width):
        #     player_p1.pos.x = SCREEN_WIDTH - player_p1.width
        # elif player_p1.pos.x <= 0:
        #     player_p1.pos.x = 0


        # Player can't move to other side of court
        # TODO reenable at end
        ### DISABLED FOR TESTING
        # if pygame.mouse.get_pos()[1] + player_p1.height <= SCREEN_HEIGHT/2:
        #     pygame.mouse.set_pos(
        #         [pygame.mouse.get_pos()[0], SCREEN_HEIGHT/2 + player_p1.height])

        # Key bindings
        buttons = pygame.mouse.get_pressed()


        # Yaw racket
        if buttons[2] and not buttons[0]:
            # yaw like this \
            player_p1.yaw = -1

        elif buttons[0] and not buttons[2]:
            # yaw like this /
            player_p1.yaw = 1
        else:
            player_p1.yaw = 0  # flat racket

        
        # Visuals
        window.blit(image_background, (0, statusbar.height))
        tennis_ball.draw(window)
        player_p1.draw(window)
        player_p2.draw(window)
        statusbar.draw(window)
        pygame.display.update()

        # update state
        state.ballPos = tennis_ball.pos
        state.ballVelocity = ball_velocity
        state.ownPos = player_p1.pos
        state.ownRacketYaw = player_p1.yaw

        # send new state to server
        server.sendall(pickle.dumps(state))


    server.close()
    pygame.quit
    sys.exit()
