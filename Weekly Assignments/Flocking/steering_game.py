##
## Author: Kristina Striegnitz
## Author: John Rieffel
## Author: Caleb L'Italien
##
## Version: Fall 2022 
##
## A character shows a simple seek behavior that makes it move towards
## a target.
##

import pygame
import random

from vector import Vector
from steering_ball import SteeringBall
from moving_ball_2d import MovingBall
from world import World

FLOCK_SIZE = 80
WIDTH = 1200
HEIGHT = 900

def run_game():
    
    ## Initialize the pygame submodules and set up the display window.
    pygame.init()
    my_win = pygame.display.set_mode((WIDTH,HEIGHT))

    ## setting up the game world
    world = World (WIDTH, HEIGHT)

    ## our characters
    flock = __make_flock()

    ## the target
    target = MovingBall (150, 175, 20, float('inf'), pygame.color.Color("red"), 0, 0)
    
    ## setting up the clock
    clock = pygame.time.Clock()
    dt = 0
    
    ## The game loop starts here.

    keepGoing = True    
    while (keepGoing):

        dt = clock.tick()
        if dt > 500:
            continue

        ## Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        mousepos = pygame.mouse.get_pos()
        mousepos = Vector(mousepos[0],mousepos[1])
        target.p = mousepos
        
        ## Simulate game world
        target.move (dt, world)
        target.collide_edge (world)

        center_x, center_y = __center_of_flock(flock)
        velocity_x, velocity_y = __flock_average_velocity(flock)

        centroid = MovingBall(center_x, center_y, 20, float('inf'), pygame.color.Color("red"), 0, 0)

        for flocker in flock:
            flocker.steering = []
            flocker.arrive(target, 1.0/30)
            flocker.cohesion(centroid, 1.0/30)
            flocker.separation(flock, 1.0/30)
            flocker.align((velocity_x, velocity_y), 1.0/30)

            flocker.apply_steering()
            flocker.move(dt, world)
            flocker.collide_edge (world)

        ## Rendering
        # Draw frame
        my_win.fill(pygame.color.Color("gray14"))

        target.draw(my_win)
        for flocker in flock:
            flocker.draw(my_win)

        # Swap display
        pygame.display.update()

    ## The game loop ends here.

    pygame.quit()


def __make_flock():
    flock = []
    while len(flock) < FLOCK_SIZE:
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)

        flocker = SteeringBall(x, y, 10, 1, pygame.color.Color("darkorange"), 0, 0)
        flock.append(flocker)
    return flock

def __center_of_flock(flock):
    x = 0
    y = 0
    for flocker in flock:
        x = x + flocker.p.x
        y = y + flocker.p.y
    return (x / FLOCK_SIZE), (y / FLOCK_SIZE)

def __flock_average_velocity(flock):
    x = 0
    y = 0
    for flocker in flock:
        x = x + flocker.v.x
        y = y + flocker.v.y
    return (x / FLOCK_SIZE), (y / FLOCK_SIZE)

## Start game
run_game()
