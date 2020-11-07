# Made with python 3.8

import pygame
import os 
import sys
from client import ball
from client import player
from client import statusbar

os.environ['SDL_VIDEO_CENTERED'] = '1'  # center window on screen

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000

BALL_WIDTH = 20
BALL_HEIGHT = 20
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 10

collisionNo = 0

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tennis game")
clock = pygame.time.Clock()

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

def redrawGameWindow():
    pygame.display.update()


def main():
    pass

statusbar = statusbar.Statusbar(SCREEN_WIDTH, 30)
tennis_ball = ball.Ball()
player_p1 = player.Player(PLAYER_WIDTH, PLAYER_HEIGHT)

court_color = (0,133,102)
court_stripes = (255,255,255)

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
    window.fill(court_color)
    statusbar.draw(window)
    tennis_ball.draw(window)
    player_p1.draw(window)
    pygame.draw.aaline(window, court_stripes, (0, SCREEN_HEIGHT/2), (SCREEN_WIDTH, SCREEN_HEIGHT/2))

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
    
    # # Player hits ball
    # if tennis_ball.x <= player_p1.x + player_p1.width and tennis_ball.x >= player_p1.x:
    #     if tennis_ball.y + tennis_ball.radius <= (player_p1.y + player_p1.height) + \
    #         (((tennis_ball.x - player_p1.x)) * player_p1.yaw_angle/100*(player_p1.yaw)) \
    #              and tennis_ball.y + tennis_ball.radius >= player_p1.y:

    #         print(tennis_ball.x , tennis_ball.y, player_p1.x, player_p1.y)
    #         print((player_p1.y + player_p1.height) + (((tennis_ball.x-player_p1.x))*player_p1.yaw_angle/100*(player_p1.yaw)))
   
    # Player hits ball
    # if tennis_ball.x <= player_p1.x + player_p1.width and tennis_ball.x >= player_p1.x:
    #     if player_p1.yaw == 0:
    #       if tennis_ball.y + tennis_ball.radius <= (player_p1.y + player_p1.height)\
    #             and tennis_ball.y + tennis_ball.radius >= player_p1.y:
    #             print("flat")
    #     elif player_p1.yaw == -1:
    #         if tennis_ball.y + tennis_ball.radius <= (player_p1.y + player_p1.height) + (((tennis_ball.x-player_p1.x))*player_p1.yaw_angle/100*(player_p1.yaw))\
    #             and tennis_ball.y + tennis_ball.radius >= player_p1.y:
    #             print("\\")
    #     elif player_p1.yaw == 1:
    #         if tennis_ball.y + tennis_ball.radius <= (player_p1.y + player_p1.height) + (((tennis_ball.x-player_p1.x))*player_p1.yaw_angle/100*(player_p1.yaw))\
    #             and tennis_ball.y + tennis_ball.radius >= player_p1.y:
    #             print("/")

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

<<<<<<< HEAD
    # yaw racket
=======
    # Yaw racket
>>>>>>> mechanics
    if keys[pygame.K_a]:
        # yaw like this \
        player_p1.yaw = -1

    elif keys[pygame.K_d]:
        # yaw like this /
        player_p1.yaw = 1
<<<<<<< HEAD

    if not(keys[pygame.K_a] or keys[pygame.K_d]):  # reset yaw from \ or / to _
        player_p1.yaw = 0




   # Player hits ball
    if tennis_ball.x <= player_p1.x + player_p1.width and tennis_ball.x >= player_p1.x:
        if player_p1.yaw == 0:
          if tennis_ball.y + tennis_ball.radius <= (player_p1.y + player_p1.height)\
             and tennis_ball.y + tennis_ball.radius >= player_p1.y:
              print("flat")
        elif player_p1.yaw == -1:
            if tennis_ball.y + tennis_ball.radius <= (player_p1.y + player_p1.height) - (((tennis_ball.x-player_p1.x))*player_p1.yaw_angle/100*(player_p1.yaw))\
             and tennis_ball.y + tennis_ball.radius >= player_p1.y - (((tennis_ball.x-player_p1.x))*player_p1.yaw_angle/100*(player_p1.yaw)):
              print("\\")
        elif player_p1.yaw == 1:
            if tennis_ball.y + tennis_ball.radius <= (player_p1.y + player_p1.height) + (((tennis_ball.x-player_p1.x))*player_p1.yaw_angle/100)\
             and tennis_ball.y + tennis_ball.radius >= player_p1.y - (((tennis_ball.x-player_p1.x))*player_p1.yaw_angle/100):
              print("/")

=======

    if not(keys[pygame.K_a] or keys[pygame.K_d]):  # reset yaw from \ or / to _
        player_p1.yaw = 0
    



>>>>>>> mechanics
    """
     something like:
        if tennis_ball.x is within player's hitbox x-values (x position and width):
            if (ball.y+ball.radius) is within player's hitbox y-values(y position and height/2):
                ball hits player, direction is shifted ( velocity * (-1)) (and direction changed if yawed etc)
    """

    """
        something like:
        if ball.x >= SCREEN_WIDTH or ball.x <= 0 or ball.y >= SCREEN_HEIGHT or ball.y <= 0:
            doSomethingCoolHere()

    """






    # Update screen
    redrawGameWindow()
""" main loop end """


if __name__ == "__main__":
    main()
