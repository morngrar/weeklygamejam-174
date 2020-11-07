from client import *
import os
import pygame

image_ball_original = pygame.image.load(os.path.join('resources', 'pytennis_ball.png'))
image_ball = pygame.transform.scale(image_ball_original, (30, 30))

class Ball:
    def __init__(self):
        self.x = 400
        self.y = 600
        self.z = 0
        self.radius = 15
        self.ball_color = (220, 253, 80)
    

    def draw(self, window):
        # pygame.draw.circle(window, self.ball_color, (self.x, self.y), self.radius)
        window.blit(image_ball, (self.x, self.y))
        

    def move_x(self, x):
        self.x += x
    
    def move_y(self, y):
        self.y += y
