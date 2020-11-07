from client import *
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1280

class Ball:
    def __init__(self):
        self.radius = 15
        self.ball_color = (220, 253, 80)
        self.pos = pygame.math.Vector3(400,600,0)

    

    def draw(self, window):
        pygame.draw.circle(window, self.ball_color, (int(self.pos.x), int(self.pos.y)), self.radius)


    
