##
## Author: Caleb L'Italien
##
## 09.28.22
##
## A brick
##
import pygame

from vector import Vector

class Brick:
    p = Vector(0.0,0.0)
    m = 0.0

    color = pygame.color.Color('darkgreen')

    def __init__(self, x, y, m, color, width, height, invincible):
        self.p = Vector(float(x), float(y))
        self.m = float(m)
        self.color = color
        self.width = width
        self.height = height
        self.invincible = invincible

    def draw(self, window):
        pygame.draw.rect(window, self.color, (int(self.p.x),int(self.p.y), self.width, self.height))

    def getRect_p(self):
        return self.p

    def getColor(self):
        return self.color

    def isInvincible(self):
        return self.invincible

