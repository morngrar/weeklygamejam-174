from client import *
import pygame

class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 20
        self.height = 20
        self.ball_color = (220, 253, 80)

    def draw(self, window):
        pygame.draw.ellipse(window, self.ball_color, self)
