##
## Author: Caleb L'Italien
##
## 09.28.22
##
## A static rectangle
##
import pygame

from vector import Vector

class Rectangle:
    p = Vector(0.0,0.0)
    m = 0.0

    color = pygame.color.Color('darkgreen')

    def __init__(self, x, y, m, color, width, height):
        self.p = Vector(float(x), float(y))
        self.m = float(m)
        self.color = color
        self.width = width
        self.height = height

    def draw(self, window):
        pygame.draw.rect(window, self.color, (int(self.p.x),int(self.p.y), self.width, self.height))

