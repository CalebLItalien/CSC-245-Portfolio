##
## Author: Kristina Striegnitz, John Rieffel, Caleb L'Italien
##
## Version: Fall 2022
##
## This file defines a simple ball class. The ball is stationary; we
## just get to define its position, size and color. This
## implementation uses the vector class.

import pygame
import random


class Ball:

    #initialize state variables

    def __init__ (self, x, y, r, m, color):
        self.x = x
        self.y = y
        self.xv = 0
        self.yv = 0
        self.r = r
        self.m = float(m)
        self.color = color

    def setVelocity(self,inVelocityX,inVelocityY):
        self.xv, self.yv = inVelocityX,inVelocityY

    def draw (self, window):
        pygame.draw.circle(window, self.color, (int(self.x),int(self.y)),self.r)

    def simulate(self, width, height):
        self.updatePosition()
        self.bounce(width, height)

    def setColor(self, newColor):
        self.color = newColor

    def randomizePosition(self, width, height):
        self.x = random.randint(0,width)
        self.y = random.randint(0,height)
    
    def changeXDirection(self):
        self.xv *= -1

    def changeYDirection(self):
        self.yv *= -1

    def bounce(self, width, height):
        if self.x + self.r >= width:
            self.changeXDirection()
            self.x = width - self.r
        elif self.x - self.r <= 0:
            self.changeXDirection()
            self.x = self.r
        elif self.y + self.r >= height:
            self.changeYDirection()
            self.y = height - self.r
        elif self.y - self.r <= 0:
            self.changeYDirection()
            self.y = self.r
    
    def updatePosition(self):
        self.x = self.x + self.xv
        self.y = self.y + self.yv