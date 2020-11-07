from client import *
import pygame


class Player:
    def __init__(self, width, height):
        self.x = 640
        self.y = 760
        self.z = 0
        self.width = width
        self.height = height
        self.player_color = (210, 105, 30)
        self.yaw = 0       # Which way to rotate: -1 = \ , 0 = __ , 1 = /
        self.yaw_angle = 25     # How many degrees to rotate in the horizontal plane, as seen top down
        self.image = pygame.Surface((80, 10))
        self.image.set_colorkey((0, 0, 0))  # make background of player invisible when rotating
        self.image.fill(self.player_color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.width // 2 , self.height // 2)

    def draw(self, window):
        old_center = self.rect.center
        rot = self.yaw_angle*self.yaw
        new_image = pygame.transform.rotate(self.image, rot)
        self.rect = new_image.get_rect()
        self.rect.center = old_center
        window.blit(new_image, (self.x, self.y))

    def move(self, x, y):
        self.x = x - (self.width/2)
        self.y = y - (self.height/2)