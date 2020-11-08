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
os.environ['SDL_VIDEO_CENTERED'] = '1'  # center window on screen


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
    
    
p1 = 1
opponent = 2
p1_score = 0
opponent_score = 0
winning_score = 3#15
   
def reset_scores():
    global p1_score
    global opponent_score
    p1_score = 0
    opponent_score = 0


        
def main():

    print("\n\nWaiting for an opponent...")

    #
    ## internal functions

    def add_point(p):
        """Adds point to the respective player"""

        nonlocal statusbar
        global p1_score
        global opponent_score
        if p == 1:
            p1_score += 1
            p2_serve()
        else:
            opponent_score += 1
            p1_serve()


    def p1_serve():
        nonlocal ball_velocity
        tennis_ball.pos.x = screen.WIDTH / 2
        tennis_ball.pos.y = screen.HEIGHT*0.75
        ball_velocity = Vector2(0, 0)

    def p2_serve():
        nonlocal ball_velocity
        tennis_ball.pos.x = screen.WIDTH / 2
        tennis_ball.pos.y = screen.HEIGHT*0.25
        ball_velocity = Vector2(0, 0)

    def check_if_someone_won():
        nonlocal state
        global winning_score
        global p1_score
        global opponent_score

        if p1_score == winning_score or opponent_score == winning_score:
            state.gameOver = True
        

           

    def show_end_screen():
        global p1_score
        global opponent_score
        global winning_score
        nonlocal window

        font = pygame.font.SysFont('comicsans', 30, True, False)

        s = pygame.Surface((screen.WIDTH,screen.HEIGHT))  # the size of your rect
        s.set_alpha(128)                # alpha level
        s.fill((0,0,0))           # this fills the entire surface
        window.blit(s, (0,0))    # (0,0) are the top-left coordinates

        winner = ""
        if p1_score == winning_score:
            text = font.render(("You won"), 1, (255, 255, 255))
        else:
            text = font.render(("You lost"), 1, (255, 255, 255))

        xpos = screen.WIDTH/2 - text.get_width()/2
        ypos = screen.HEIGHT/2 - text.get_height()/2

        window.blit(text, (xpos, ypos))
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

    pygame.mouse.set_visible(False)

    p1_serve()



    #
    ## Handshake and start game loop

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

    window = pygame.display.set_mode((screen.WIDTH, screen.HEIGHT))
    pygame.display.set_caption("Tennis game")
    clock = pygame.time.Clock()
    statusbar = Statusbar(screen.WIDTH, 30)
    
    while run:
        clock.tick(200)     # refresh rate
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
        global p1_score
        global opponent_score
        p1_score = state.ownPoints
        opponent_score = state.opponentPoints

        # Update status bar
        statusbar.playerscore = p1_score
        statusbar.opponentscore = opponent_score

        player_p2.pos = state.opponentPos
        player_p2.pos = flip_coords(player_p2.pos)
        player_p2.pos.x -= player_p2.width
        player_p2.pos.y -= player_p2.height
        player_p2.yaw = state.opponentRacketYaw
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

            if ball_velocity.y != 0 and not state.gameOver:
                # Check whose player's side of the court the ball has been played out on
                # If the ball was played out on the opponents side, add point to me
                if tennis_ball.pos.y <= (screen.HEIGHT/2): 
                    add_point(p1)   # Add point to "me"
                    
                else: 
                    add_point(opponent) # Add point to opponent
        
            check_if_someone_won()

        ##########################################################s



        line = player_p1.get_center_line()
        distance_to_ball = dist(line, tennis_ball.pos.x, tennis_ball.pos.y)

        # If the ball is on player's side            # and distance is small enough to ball
        if tennis_ball.pos.y >= screen.HEIGHT/2 and distance_to_ball <= tennis_ball.radius:
            if ball_velocity.y >= 0:
                ball_velocity = Vector2(player_p1.vel) - ball_velocity 

                # adds a vector force for paddle yaw
                ball_velocity += (YAW_VELOCITY + YAW_ANGLING * player_p1.yaw) * YAW_ACCEL 

                # decelerate (slows down ball if paddle is still)
                ball_velocity *= 0.6

                # if speed isn't limited, paddle can clip through ball
                if ball_velocity.magnitude() > BALL_MAX_SPEED:       
                    ball_velocity *= 0.5

        player_p1.move(*(pygame.mouse.get_pos()))   # Paddle moves after mouse

        if i > 10:   # for velocity to not be 0, only sample intermittently
            player_p1.last_pos = Vector2(player_p1.pos)
            i = 0
        player_p1.vel = (player_p1.pos - player_p1.last_pos)*2

        tennis_ball.pos += ball_velocity * BALL_FRICTION_FACTOR

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
        
        if state.gameOver:
            show_end_screen()
        pygame.display.update()

        # update state
        state.ownPoints = p1_score
        state.opponentPoints = opponent_score
        state.ballPos = tennis_ball.pos
        state.ballVelocity = ball_velocity
        state.ownPos = player_p1.pos
        state.ownRacketYaw = player_p1.yaw

        # send new state to server
        server.sendall(pickle.dumps(state))


    server.close()
    pygame.quit
    sys.exit()
