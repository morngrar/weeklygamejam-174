
# Made with python 3.8

import pygame
from pygame.math import Vector2
import os
import sys
import pickle
import socket

from common.gamestate import GameState
from common import networking, screen, player, ball

from client.statusbar import Statusbar

pygame.init()


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()




def flip_coords(v):
    """Flips the coordinates, so that they're seen from the other side of table"""

    vector = Vector2(v)
    vector.x = screen.WIDTH - vector.x
    vector.y = screen.HEIGHT - vector.y
    return vector

image_background_original = pygame.image.load(os.path.join('resources', 'pytennis_court.png'))
image_background = pygame.transform.scale(image_background_original, (screen.WIDTH, screen.HEIGHT-30))


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
    
    
   

        
def main(p1_conn, p2_conn):

    p1 = 1
    p2 = 2
    p1_score = 0
    p2_score = 0
    winning_score = 3#15


    #
    ## internal functions

    def add_point(p):
        """Adds point to the respective player"""

        nonlocal p1_score
        nonlocal p2_score
        if p == 1:
            p1_score += 1
            p2_serve()
        else:
            p2_score += 1
            p1_serve()


    def p1_serve():
        nonlocal ball_velocity
        nonlocal p1_hit, p2_hit
        tennis_ball.pos.x = screen.WIDTH / 2
        tennis_ball.pos.y = screen.HEIGHT*0.75
        ball_velocity = Vector2(0, 0)
        p1_hit = False
        p2_hit = True

    def p2_serve():
        nonlocal ball_velocity
        nonlocal p2_hit, p1_hit
        tennis_ball.pos.x = screen.WIDTH / 2
        tennis_ball.pos.y = screen.HEIGHT*0.25
        ball_velocity = Vector2(0, 0)
        p1_hit = True
        p2_hit = False

    def check_if_someone_won():
        nonlocal state
        nonlocal winning_score
        nonlocal p1_score
        nonlocal p2_score

        if p1_score == winning_score or p2_score == winning_score:
            state.gameOver = True
        

    #
    ## pre-runloop setup
    tennis_ball = ball.Ball()
    player_p1 = player.Player()
    player_p2 = player.Player()
    player_p2.yaw_angle *= -1

    ball_velocity = Vector2()

    BALL_FRICTION_FACTOR = 0.2
    BALL_MAX_SPEED = 40

    YAW_VELOCITY = Vector2(0, -1)
    YAW_ANGLING = Vector2(-1, 0)   # positive when /
    YAW_ACCEL = 30


    p1_serve()



    #
    ## Handshake and start game loop

    run = True
    i = 0




    window = pygame.Surface((screen.WIDTH, screen.HEIGHT))

    state = GameState()
    
    from common.playerpacket import PlayerPacket


    collcnt = 0
    clock = pygame.time.Clock()
    p1_hit = False
    p2_hit = True
    while run:
        clock.tick(25)
        i+=1
        # add some deltatime instead

        # getting data from clients
        data = p1_conn.recv(networking.MAX_PACKET_SIZE)
        if not data:
            break
        packet = pickle.loads(data)
        player_p1.pos = packet.pos
        player_p1.yaw = packet.yaw

        data = p2_conn.recv(networking.MAX_PACKET_SIZE)
        if not data:
            break
        packet = pickle.loads(data)
        player_p2.pos = packet.pos
        player_p2.yaw = packet.yaw

        player_p2.pos = flip_coords(player_p2.pos)
        player_p2.pos.x -= player_p2.width
        player_p2.pos.y -= player_p2.height
        player_p2.yaw *= -1





        ###########################################################
        # Ball wall collision
        ###########################################################

        if (
            tennis_ball.pos.x + tennis_ball.radius < 0
            or tennis_ball.pos.x - tennis_ball.radius > screen.WIDTH
            or tennis_ball.pos.y + tennis_ball.radius > screen.HEIGHT
            or tennis_ball.pos.y - tennis_ball.radius < 0
        ):

            if not state.gameOver:
                # Check whose player's side of the court the ball has been played out on
                # If the ball was played out on the opponents side, add point to me
                if tennis_ball.pos.y <= (screen.HEIGHT/2): 
                    add_point(p1)   # Add point to "me"
                    
                else: 
                    add_point(p2) # Add point to opponent
        
            check_if_someone_won()

        ##########################################################s



        if tennis_ball.pos.y >= screen.HEIGHT // 2:
            line = player_p1.get_center_line()
            distance_to_ball = dist(line, tennis_ball.pos.x, tennis_ball.pos.y)
            active = player_p1
            paddle_factor = -1
            p2_hit = False
            
        else:
            line = player_p2.get_center_line()
            distance_to_ball = dist(line, tennis_ball.pos.x, tennis_ball.pos.y)
            active = player_p2
            paddle_factor = 1
            p1_hit = False


        if distance_to_ball <= tennis_ball.radius:

            if active is player_p1 and not p1_hit:
                collides = True
                p1_hit = True

            elif active is player_p2 and not p2_hit:
                collides = True
                p2_hit = True
            
            else:
                collides = False


            if collides:
                paddle_vel = Vector2(active.vel.x*3, abs(active.vel.y)*paddle_factor*3)
                ball_velocity = Vector2(active.vel) - ball_velocity 

                # adds a vector force for paddle yaw
                if p1_hit and not p2_hit:
                    ball_velocity += (YAW_VELOCITY + YAW_ANGLING * active.yaw) * YAW_ACCEL 
                else:
                    ball_velocity += ((-YAW_VELOCITY) + YAW_ANGLING * active.yaw) * YAW_ACCEL 

                # decelerate (slows down ball if paddle is still)
                ball_velocity *= 0.6

                # if speed isn't limited, paddle can clip through ball
                if ball_velocity.magnitude() > BALL_MAX_SPEED:       
                    ball_velocity *= 0.5


        if i > 1:   # for velocity to not be 0, only sample intermittently
        # base this on delta time instead
            player_p1.last_pos = Vector2(player_p1.pos)
            player_p2.last_pos = Vector2(player_p2.pos)
            i=0
        player_p1.vel = (player_p1.pos - player_p1.last_pos)*6
        player_p2.vel = (player_p2.pos - player_p2.last_pos)*6

        tennis_ball.pos += ball_velocity * BALL_FRICTION_FACTOR



        
        # update state
        state.ownPoints = p1_score
        state.opponentPoints = p2_score
        state.ballPos = tennis_ball.pos
        state.opponentPos = player_p2.pos
        state.opponentRacketYaw = player_p2.yaw
        p1_conn.sendall(pickle.dumps(state))

        state.ownPoints = p2_score
        state.opponentPoints = p1_score
        state.ballPos = flip_coords(state.ballPos)
        state.opponentPos = flip_coords(player_p1.pos)
        state.opponentRacketYaw = player_p1.yaw * -1
        p2_conn.sendall(pickle.dumps(state))

        


