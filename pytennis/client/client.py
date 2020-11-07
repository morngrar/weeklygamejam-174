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


def dist(line, x3, y3):  # x3,y3 is the point
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

    # Note: If the actual distance does not matter,
    # if you only want to compare what this function
    # returns to other results of this function, you
    # can just return the squared distance instead
    # (i.e. remove the sqrt) to gain a little performance

    dist = (dx*dx + dy*dy)**.5

    return dist


def redrawGameWindow():
    pygame.display.update()


def main():
    pass

def p1_serve():
    tennis_ball.pos.x = SCREEN_WIDTH / 2
    tennis_ball.pos.y = SCREEN_HEIGHT*0.75
    ball_velocity = pygame.math.Vector3(0, 0, 0)

def p2_serve():
    tennis_ball.pos.x = SCREEN_WIDTH / 2
    tennis_ball.pos.y = SCREEN_HEIGHT*0.25
    ball_velocity = pygame.math.Vector3(0, 0, 0)

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
YAW_ACCEL = 10

pygame.mouse.set_visible(False)

p1_serve()

""" main loop """
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


    line = player_p1.get_center_line()
    start = (line[0], line[1])
    end = (line[2], line[3])
    pygame.draw.line(window, (200, 200, 0), start, end)



    # Ball wall collision
    if tennis_ball.pos.x + tennis_ball.radius >= SCREEN_WIDTH or tennis_ball.pos.x <= 0 + tennis_ball.radius:
        tennis_ball.pos.x = SCREEN_WIDTH / 2
        tennis_ball.pos.y = SCREEN_HEIGHT*0.75
        ball_velocity = pygame.math.Vector3(0, 0, 0)

    if tennis_ball.pos.y <= 0 + tennis_ball.radius:
        ball_velocity = -(ball_velocity)

    if tennis_ball.pos.y >= SCREEN_HEIGHT:
        tennis_ball.pos.y = SCREEN_HEIGHT*0.75
        ball_velocity = pygame.math.Vector3(0, 0, 0)

    # angled distance check tactic for collision
    line = player_p1.get_center_line()
    distance_to_ball = dist(line, tennis_ball.pos.x, tennis_ball.pos.y)
    # If the ball is on player's side of court, allow for collision
    if tennis_ball.pos.y >= SCREEN_HEIGHT/2 and distance_to_ball <= tennis_ball.radius:
        if ball_velocity.y >= 0:
            ball_velocity = pygame.math.Vector3(player_p1.vel) - ball_velocity + (YAW_VELOCITY+YAW_ANGLING*player_p1.yaw)*YAW_ACCEL
            ball_velocity *= 0.6
        while ball_velocity.magnitude() > BALL_MAX_SPEED:
            ball_velocity *= 0.9

    player_p1.move(*(pygame.mouse.get_pos()))   # Player moves after mouse
    if i > 5:
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
    keys = pygame.key.get_pressed()

    # Yaw racket
    if keys[pygame.K_a]:
        # yaw like this \
        player_p1.yaw = -1

    elif keys[pygame.K_d]:
        # yaw like this /
        player_p1.yaw = 1

    if not(keys[pygame.K_a] or keys[pygame.K_d]):  # reset yaw from \ or / to _
        player_p1.yaw = 0

    # Update screen
    # Visuals
    window.fill(court_color)
    pygame.draw.aaline(window, court_stripes,
                       (0, SCREEN_HEIGHT/2), (SCREEN_WIDTH, SCREEN_HEIGHT/2))
    tennis_ball.draw(window)
    player_p1.draw(window)
    redrawGameWindow()
""" main loop end """


if __name__ == "__main__":
    main()
