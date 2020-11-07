from client import *
import pygame


class Statusbar:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.color = (0, 0, 0)

    def draw(self, window):
        pygame.Surface.fill(window, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('comicsans', 30, True, False)
        text = font.render("heihei", 1, (255, 255, 255))
        window.blit(text, (round(text.get_width()/4), round(self.height/2 - (text.get_height()/2))))
