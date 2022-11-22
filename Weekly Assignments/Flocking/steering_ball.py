##Author: Caleb L'Italien


import pygame
from moving_ball_2d import MovingBall
from vector import Vector

THRESHOLD = 4

class SteeringBall (MovingBall):

    beak_tip = Vector(0,20)

    speedlimit = Vector(4000,4000)

    # All steering inputs
    steering = []

    def draw (self, window):
        # draw the body
        pygame.draw.circle(window, self.color, (int(self.p.x),int(self.p.y)),self.r)
        # draw the beak
        speed = self.v.length()
        if speed != 0:
            self.beak_tip = self.v.normalize() * 20
        pygame.draw.line(window,self.color,(int(self.p.x),int(self.p.y)),(self.p.x+self.beak_tip.x,self.p.y+self.beak_tip.y), 3)

        if self.drawvec:
            for vec in self.steering:
                arrowvec = Vector(0,0)
                arrowvec = arrowvec + vec
                arrowvec = arrowvec + self.p
                #pygame.draw.line(window,pygame.color.Color("red"),(int(self.p.x),int(self.p.y)),(arrowvec.x,arrowvec.y),2)


    def __str__ (self):
        return str(self.p)+", "+str(self.v)+", "+str(self.a) 


    def apply_steering (self):
        ## add all steering inputs to current velocity vector
        for s in self.steering:
            self.v += s


    def seek (self, target, weight):

        #find difference between my location and target location 
        desired_direction = (target.p - self.p).normalize()
        #multiply direction by max speed
        max_speed = self.speedlimit.length()
        desired_velocity = desired_direction * max_speed
        ## first find the "error" between current velocity and desired velocity, and then multiply that error 
        ## by the weight, and then add it to steering inputs
        self.steering += [(desired_velocity - self.v)*weight]

    def arrive(self, target, weight):
        desired_direction = (target.p - self.p).normalize()
        max_speed = self.speedlimit.length()

        distance = (target.p - self.p).length()
        sum_radii = target.r + self.r
        distance_proportion = distance / (sum_radii * THRESHOLD)

        if (sum_radii * THRESHOLD) < distance:
            desired_velocity = desired_direction * max_speed
        else:
            desired_velocity = desired_direction * distance_proportion * max_speed
        self.steering += [(desired_velocity - self.v) * weight]

    def flee(self, target, weight):
        desired_direction = -1 * (target.p - self.p).normalize()
        max_speed = self.speedlimit.length()

        distance = (target.p - self.p).length()
        sum_radii = target.r + self.r
        distance_proportion = (sum_radii * THRESHOLD) / distance

        if (sum_radii * THRESHOLD) > distance:
            desired_velocity = desired_direction * distance_proportion * max_speed
            self.steering += [(desired_velocity - self.v) * weight]

    def cohesion(self, centroid, weight):
        desired_direction = (centroid.p - self.p).normalize()
        max_speed = self.speedlimit.length()
        desired_velocity = desired_direction * max_speed
        self.steering += [(desired_velocity - self.v) * weight]

    def separation(self, flock, weight):
        vector_adjustment = Vector(0,0)
        for flocker in flock:
            if self != flocker:
                distance = self.p - flocker.p
                sum_radii = (self.r + flocker.r) * 1.5

                if distance.length() < sum_radii:
                    direction = (self.p - flocker.p).normalize()
                    max_speed = self.speedlimit.length()

                    adjustment = direction * max_speed
                    vector_adjustment = vector_adjustment - adjustment

                    self.steering += [(self.v - vector_adjustment) * weight]
                    flocker.steering += [(-1) * (flocker.v - vector_adjustment) * weight]

    def align(self, average_velocity, weight):
        velocity_x, velocity_y = average_velocity
        vector_average = Vector(velocity_x, velocity_y)

        difference = self.v - vector_average
        max_speed = self.speedlimit.length()

        adjustment = difference * max_speed
        self.steering += [(self.v - adjustment) * weight]
