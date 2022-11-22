##
## Author: Kristina Striegnitz
##
## Version: Fall 2011 
##
## Illustrates collision balls.
## Starter code for Breakout
##

import pygame
import random

from moving_ball_sprite_2d import MovingBall
from vector import Vector

def run_game():
    
    ## Initialize the pygame submodules and set up the display window.

    pygame.init()

    balls= []
    
    width = 640
    height = 480
    my_win = pygame.display.set_mode((width,height))

    ## important properties of the environment
    env = {'ground':height, 'g':100.0}

    ## initialize the balls
    numballs = 2

    b1 = MovingBall (20, 10+height/2, 20, 20, pygame.color.Color("darkmagenta"), .1, .1)
    b2 = MovingBall (200, height/2, 10, 10, pygame.color.Color("darkorange"), -.1, .1)
    balls.append(b1)
    balls.append(b2)
    # elasticity coefficient
    e = 1.0
    
    ## setting up the clock
    clock = pygame.time.Clock()
    dt = 0
    
    ## The game loop starts here.

    keepGoing = True    
    while (keepGoing):


        #dt = clock.tick(50)
        #print dt

        ## Handle events.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                

        ## Simulate game world
        for b in balls:
            b.simulate(dt, width, height)


        ##  https://www.vobarian.com/collisions/2dcollisions2.pdf
        ##  https://ericleong.me/research/circle-line/
        for i in range(0,len(balls)):
            b1 = balls[i]
            for j in range(i+1,len(balls)):
                b2 = balls[j]
               #calculate normal of collission
                n = b1.collide(b2)
                if n != None:
                    #print "hit!", b1.p, " ", b2.p
                    # new velocity is 
                    # v_normal' = v_normal*(m1-m2)+2*m2*v2_normal
                    #              ----------------------------      
                    #                   m1 + m2
                    #print("normvector:", n)
                    print("do something here")
                        
                


       
        #print b1.v

        ## Draw frame
        
        my_win.fill(pygame.color.Color("gray14"))


        for b in balls:
                b.draw(my_win)

        ## Swap display

        pygame.display.update()

    ## The game loop ends here.

    pygame.quit()


## Start game
run_game()
