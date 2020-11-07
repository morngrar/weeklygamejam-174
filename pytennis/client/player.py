from client import *
import pygame

from math import sin, cos, radians


class Player:
    def __init__(self, width, height):
        self.pos = pygame.math.Vector3(640,760,0)
        self.vel = pygame.math.Vector3(0,0,0)
        self.last_pos = pygame.math.Vector3(self.pos)
        self.width = width
        self.height = height
        self.player_color = (210, 105, 30)
        self.yaw = 0       # Which way to rotate: -1 = \ , 0 = __ , 1 = /
        self.yaw_angle = 25     # How many degrees to rotate in the horizontal plane, as seen top down
        self.image = pygame.Surface((80, 10))
        self.image.set_colorkey((0, 0, 0))  # make background of player invisible when rotating
        self.image.fill(self.player_color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.width // 2, self.height // 2)

    def get_center_line(self):
        x1 = self.pos.x
        x2 = self.pos.x + self.width
        y1 = self.pos.y + self.height/2
        y2 = y1

        cx = 0
        cy = self.pos.y+self.height

        if self.yaw > 0:
            cx = x2
        elif self.yaw < 0:
            cx = x1
        
        deg = self.yaw_angle*self.yaw
        theta = radians(deg)
        cosang = cos(theta)
        sinang = sin(theta)

        tx1 = self.pos.x-cx
        ty1 = self.pos.y-cy
        p1x = ( tx1*cosang + ty1*sinang) + cx
        p1y = (-tx1*sinang + ty1*cosang) + cy
        tx2 = self.pos.x + self.width-cx
        ty2 = self.pos.y-cy
        p2x = ( tx2*cosang + ty2*sinang) + cx
        p2y = (-tx2*sinang + ty2*cosang) + cy

        return (p1x, p1y, p2x, p2y)

    def draw(self, window):
        old_center = self.rect.center
        rot = self.yaw_angle*self.yaw
        new_image = pygame.transform.rotate(self.image, rot)
        self.rect = new_image.get_rect()
        self.rect.center = old_center
        window.blit(new_image, (self.pos.x, self.pos.y))

    def move(self, x, y):
        self.pos.x = x #- (self.width/2)
        self.pos.y = y #- (self.height/2)
