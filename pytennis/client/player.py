from client import *
import pygame

class Player:
    def __init__(self):
        self.x = 640
        self.y = 760
        self.width = 40
        self.height = 30
        self.player_color = (210,105,30)

    def draw(self, window):
        pygame.draw.rect(window, self.player_color, (self.x, self.y, self.width, self.height))

    def move(self, x, y):
        self.x = x - (self.width/2)
        self.y = y - (self.height/2)