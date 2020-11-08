from client import *
import os
import pygame

image_ball_original = pygame.image.load(os.path.join('resources', 'pytennis_ball.png'))
image_ball = pygame.transform.scale(image_ball_original, (30, 30))

class Ball:
    def __init__(self):
        self.radius = 15
        self.ball_color = (220, 253, 80)
        self.pos = pygame.math.Vector3(400,600,0)

    def draw(self, window):
        window.blit(image_ball, (int(self.pos.x), int(self.pos.y)))
