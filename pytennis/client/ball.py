from client import *
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1280

class Ball:
    def __init__(self):
        self.x = 400
        self.y = 600
        self.z = 0
        self.radius = 15
        self.ball_color = (220, 253, 80)
    

    def draw(self, window):
        pygame.draw.circle(window, self.ball_color, (self.x, self.y), self.radius)

    def move_x(self, x):
        self.x += x
    
    def move_y(self, y):
        self.y += y
