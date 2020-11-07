# Made with python 3.8

import pygame
import os 
import sys
from client import ball
from client import player
from client import statusbar

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'  # center window on screen

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1310

BALL_WIDTH = 20
BALL_HEIGHT = 20
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 10

collisionNo = 0

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tennis game")
clock = pygame.time.Clock()

image_background_original = pygame.image.load(os.path.join('resources', 'pytennis_court.png'))
image_background = pygame.transform.scale(image_background_original, (SCREEN_WIDTH, SCREEN_HEIGHT-30))



def dist(line, x3, y3): # x3,y3 is the point
    x1, y1, x2, y2 = line
    px = x2-x1
    py = y2-y1

    norm = px*px + py*py
    if norm == 0:
        return None

    u =  ((x3 - x1) * px + (y3 - y1) * py) / float(norm)

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


def main():
    pass

statusbar = statusbar.Statusbar(SCREEN_WIDTH, 30)
tennis_ball = ball.Ball()
player_p1 = player.Player(PLAYER_WIDTH, PLAYER_HEIGHT)

#Ball speed, remove later
ball_speed_x = 0
ball_speed_y = 0

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
    window.blit(image_background, (0, statusbar.height))
    statusbar.draw(window)
    tennis_ball.draw(window)
    player_p1.draw(window)

    # line = player_p1.get_center_line()
    # start = (line[0], line[1])
    # end = (line[2], line[3])
    # pygame.draw.line(window, (200, 200, 0), start, end)

    # Mechanics
    player_p1.move(*(pygame.mouse.get_pos()))   # Player moves after mouse
    pygame.mouse.set_visible(False)
    tennis_ball.move_x(ball_speed_x)
    tennis_ball.move_y(ball_speed_y)
    
    # Ball wall collision
    if tennis_ball.x >= SCREEN_WIDTH + tennis_ball.radius or tennis_ball.x <= 0 + tennis_ball.radius:
        ball_speed_x *= -1
        tennis_ball.move_x(ball_speed_x)
    
    if tennis_ball.y >= SCREEN_HEIGHT + tennis_ball.radius or tennis_ball.y <= 0 + tennis_ball.radius:
        ball_speed_y *= -1
        tennis_ball.move_y(ball_speed_y)
    

    # angled distance check tactic for collision
    line = player_p1.get_center_line()
    distance_to_ball = dist(line, tennis_ball.x, tennis_ball.y)
    if distance_to_ball <= tennis_ball.radius:
        collisionNo += 1
        print("COLLISION!", collisionNo)

    # Player can't move to other side of court or "out of window"
    if player_p1.x >= SCREEN_WIDTH - (player_p1.width*2):
        player_p1.x = SCREEN_WIDTH - player_p1.width 
    elif player_p1.x <= 0:
        player_p1.x = 0
    
    if player_p1.y <= SCREEN_HEIGHT/2 or player_p1.y <= 0:
        player_p1.y = SCREEN_HEIGHT/2

    
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
    pygame.display.update()
""" main loop end """


if __name__ == "__main__":
    main()
