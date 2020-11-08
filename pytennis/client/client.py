# Made with python 3.8

import pygame
import os
import sys
from tkinter import *
from tkinter import messagebox

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


def show_end_screen():
    global p1_score
    global opponent_score
    global winning_score
    winner = ""
    if p1_score == winning_score:
        winner = "YOU WON"
    else:
        winner = "OPPONENT WON"

    Tk().wm_withdraw() #to hide the main window
    res = messagebox.askquestion(winner,  
                         'New Game?') 
    if res == 'yes' : 
        reset_scores()          
    else: 
        pygame.quit
        sys.exit()
    
    
   
def reset_scores():
    global p1_score
    global opponent_score
    p1_score = 0
    opponent_score = 0

def check_if_someone_won():
    global winning_score
    global p1_score
    global opponent_score

    if(p1_score == winning_score):
        show_end_screen()
    elif(opponent_score == winning_score):
        show_end_screen()

def main():
    pass

def p1_serve():
    global ball_velocity
    tennis_ball.pos.x = SCREEN_WIDTH / 2
    tennis_ball.pos.y = SCREEN_HEIGHT*0.75
    ball_velocity = pygame.math.Vector3(0, 0, 0)

def p2_serve():
    global ball_velocity
    tennis_ball.pos.x = SCREEN_WIDTH / 2
    tennis_ball.pos.y = SCREEN_HEIGHT*0.25
    ball_velocity = pygame.math.Vector3(0, 0, 0)

p1 = 1
opponent = 2
p1_score = 0
opponent_score = 0
winning_score = 3


# Adds point to the respective player
def add_point(p):
    global p1_score
    global opponent_score
    if p == 1:
        p1_score += 1
        print("You scored! You have ", p1_score, " points")
        p1_serve()
    else:
        opponent_score += 1
        print("Opponent scored! Opponent has ", opponent_score, " points")
        p2_serve()


tennis_ball = ball.Ball()
player_p1 = player.Player(PLAYER_WIDTH, PLAYER_HEIGHT)

court_color = (0, 133, 102)
court_stripes = (255, 255, 255)

# Ball speed, remove later
ball_velocity = pygame.math.Vector3()

BALL_FRICTION_FACTOR = 0.2
BALL_MAX_SPEED = 40

YAW_VELOCITY = pygame.math.Vector3(0, -1, 0)
YAW_ANGLING = pygame.math.Vector3(-1, 0, 0)   # positive when /
YAW_ACCEL = 30

pygame.mouse.set_visible(False)



p1_serve()

run = True
i = 0
while run:

    clock.tick(100)
    i += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit
            sys.exit()



    ###########################################################
    # Ball wall collision -- remove when ready for multiplayer
    ###########################################################
    if (    # If the ball is played out on either side 
        tennis_ball.pos.x + tennis_ball.radius >= SCREEN_WIDTH 
        or tennis_ball.pos.x <= 0 + tennis_ball.radius
    ):
        # Check whose player's side of the court the ball has been played out on
        # If the ball was played out on the opponents side, add point to me
        if tennis_ball.pos.y <= (SCREEN_HEIGHT/2): 
            add_point(p1)   # Add point to "me"
            
        else: 
            add_point(opponent) # Add point to opponent
    
    check_if_someone_won()

    if tennis_ball.pos.y <= 0 + tennis_ball.radius:
        ball_velocity = -(ball_velocity)
        #add_point(p1)

    if tennis_ball.pos.y >= SCREEN_HEIGHT:
        tennis_ball.pos.y = SCREEN_HEIGHT*0.75
        ball_velocity = pygame.math.Vector3(0, 0, 0)
        #add_point(opponent)
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
            ball_velocity = pygame.math.Vector3(player_p1.vel) - ball_velocity 

            # adds a vector force for paddle yaw
            ball_velocity += (YAW_VELOCITY + YAW_ANGLING * player_p1.yaw) * YAW_ACCEL 

            # decelerate (slows down ball if paddle is still)
            ball_velocity *= 0.6

        # if speed isn't limited, paddle can clip through ball
        while ball_velocity.magnitude() > BALL_MAX_SPEED:       
            ball_velocity *= 0.9

    player_p1.move(*(pygame.mouse.get_pos()))   # Paddle moves after mouse

    if i > 5:   # for velocity to not be 0, only sample intermittently
        player_p1.last_pos.x, player_p1.last_pos.y = player_p1.pos.x, player_p1.pos.y
        i = 0
    player_p1.vel = (player_p1.pos - player_p1.last_pos)*2

    tennis_ball.pos += ball_velocity * BALL_FRICTION_FACTOR



    # Player can't move to other side of court or "out of window"
    if player_p1.pos.x >= SCREEN_WIDTH - (player_p1.width):
        player_p1.pos.x = SCREEN_WIDTH - player_p1.width
    elif player_p1.pos.x <= 0:
        player_p1.pos.x = 0



    # Player can't move to other side of court
    if pygame.mouse.get_pos()[1] + player_p1.height <= SCREEN_HEIGHT/2:
        pygame.mouse.set_pos(
            [pygame.mouse.get_pos()[0], SCREEN_HEIGHT/2 + player_p1.height])

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

    # Update screen
    # Visuals
    window.fill(court_color)
    pygame.draw.aaline(window, court_stripes,
                       (0, SCREEN_HEIGHT/2), (SCREEN_WIDTH, SCREEN_HEIGHT/2))
    tennis_ball.draw(window)
    player_p1.draw(window)
    pygame.display.update()


if __name__ == "__main__":
    main()