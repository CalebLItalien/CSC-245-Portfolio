##
## Author: Caleb L'Italien
##
## 09.28.22
##
## A moving rectangle
##
from rect_2d import Rectangle

SIDE_BUFFER = 10
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

class Paddle(Rectangle):
    def __init__(self, x, y, m, color, width, height):
        Rectangle.__init__(self, x, y, m, color, width, height)

    def moveLeft(self, length):
        self.p.x -= length
        if self.p.x < SIDE_BUFFER:
            self.p.x = SIDE_BUFFER

    def moveRight(self, length):
        self.p.x += length
        if self.p.x > ((WINDOW_WIDTH - SIDE_BUFFER) - self.width):
            self.p.x = (WINDOW_WIDTH - SIDE_BUFFER) - self.width

    def position_x(self):
        return self.p.x

    def position_y(self):
        return self.p.y






