from client import *
import pygame

class Ball:
    def __init__(self):
        self.x = 640
        self.y = 400
        self.radius = 15
        self.ball_color = (220, 253, 80)

    def draw(self, window):
        pygame.draw.circle(window, self.ball_color, (self.x - self.radius, self.y - self.radius), self.radius)
