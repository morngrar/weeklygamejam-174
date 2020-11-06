from client import *
import pygame

class Ball:
    def __init__(self):
        self.x = 640
        self.y = 400
        self.radius = 10
        self.ball_color = (220, 253, 80)

    def draw(self, window):
        pygame.draw.ellipse(window, self.ball_color, (x - radius, y - radius), radius)
