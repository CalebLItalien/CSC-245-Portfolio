##
## Author: Kristina Striegnitz
##
## Version: Fall 2011 
##
## Updates: John Rieffel, Fall 2022, Caleb L'Italien, September 2022
##
## This file defines a ball class that can move in two dimensions and
## can bounce off other objects

from vector import Vector
from ball_2d import Ball

X_DEFAULT = 300
Y_DEFAULT = 500
DEFAULT_X_SPEED = -1.5
DEFAULT_Y_SPEED = 1.5
BORDER_BUFFER = 4

class MovingBall (Ball):

    v = Vector(0.0, 0.0)

    speedlimit = 5

    def __init__ (self, x, y, r, m, color, xv, yv):

        Ball.__init__(self, x, y, r, m, color)

        self.v = Vector(float(xv),float(yv))


    def simulate (self, dt, width, height):
        self.move (dt)
        self.bounce_wall (width, height)


    def move (self, dt):
        self.p = self.p + self.v


    def clamp_v (self):
        '''
        clamp max speed
        '''
        if self.v.length() > self.speedlimit:
            self.v.normalize()
            self.v = self.v * float(self.speedlimit)
            

    def bounce_wall (self, width, height):
        '''
        handle bounces and readjust to prevent penetration
        '''
        if self.p.x < 0+self.r:
            self.p.x = self.r
            self.v.x *= -1

        elif self.p.x > width-self.r:
            self.p.x = width-self.r
            self.v.x *= -1


    def hit_bottom(self, height):
        if self.p.y > (height - BORDER_BUFFER)-self.r:
            self.p.x = X_DEFAULT
            self.p.y = Y_DEFAULT
            return True
        return False


    def hit_top(self):
        if self.p.y < BORDER_BUFFER + self.r:
            self.p.y = X_DEFAULT
            self.p.y = Y_DEFAULT
            return True
        return False


    def collide (self, other):
        """
        Checks whether two circles collide. If they do and are already
        intersecting, they get moved apart a bit. The return value is
        None, if there is no collision, and the vector pointing from
        the center of the first to the center of the second ball if
        there is a collision.
        """
        d = self.p - other.p
        if d.length() < self.r + other.r:
            repair = float(self.r + other.r - d.length())
            d.normalize()
            self.p = self.p + (repair*d)
            other.p = other.p + (-1*repair*d)
            return d
        else:
            return None


    def collideRect(self, rectangle):
        distance_bottom = self.p.y - (rectangle.p.y + rectangle.height)
        distance_top = self.p.y - rectangle.p.y
        distance_left = self.p.x - rectangle.p.x
        distance_right = self.p.x - (rectangle.p.x + rectangle.width)

        abs_dist_bottom = abs(distance_bottom)
        abs_dist_top = abs(distance_top)
        abs_dist_left = abs(distance_left)
        abs_dist_right = abs(distance_right)

        if abs_dist_bottom < self.r and rectangle.p.x <= self.p.x <= (rectangle.p.x + rectangle.width):
            merge = self.r + (rectangle.height / 2) - abs_dist_bottom
            self.p.y += merge
            self.reverseDirectionY()
            return ""
        if abs_dist_top < self.r and rectangle.p.x <= self.p.x <= (rectangle.p.x + rectangle.width):
            merge = self.r + (rectangle.height / 2) - abs_dist_top
            self.p.y -= merge
            self.reverseDirectionY()
            return ""
        if abs_dist_left < self.r and rectangle.p.y <= self.p.y <= (rectangle.p.y + rectangle.height):
            self.reverseDirectionX()
            return ""
        if abs_dist_right < self.r and rectangle.p.y <= self.p.y <= (rectangle.p.y + rectangle.height):
            self.reverseDirectionX()
            return ""
        return None

    def reverseDirectionY(self):
        self.v.y *= -1

    def reverseDirectionX(self):
        self.v.x *= -1

    def getResponse(self,other,normvector):
        return Vector(0,0)

    def bounce (self, j, n):
        self.v = self.v + (n * (j / self.m))
        self.clamp_v ()

    def setVelocity(self, v):
        self.v = v

    def speedUp(self):
        self.v.x *= 1.04
        self.v.y *= 1.04
        self.clamp_v()

    def slowDown(self):
        self.v.x *= 0.98
        self.v.y *= 0.98
        self.clamp_v()

    def resetSpeed(self):
        self.v.x = DEFAULT_X_SPEED
        self.v.y = DEFAULT_Y_SPEED

    def speedToString(self):
        print(self.v.x)
        print(self.v.y)

    def topSpeeds(self):
        if abs(self.v.x) > 3.0:
            return True
        return False

    def getVelocity(self):
        return self.v.x, self.v.y

    def getPosition(self):
        return self.p.x, self.p.y