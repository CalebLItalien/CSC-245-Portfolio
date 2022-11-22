# A simple pong game
# Caleb L'Italien
# Group G
#
# Original Authors: Matthew Anderson, Kristina Striegnitz, John Rieffel
# Winter 2017

import pygame
import random

def run_game():

    # Initialize pygame and set up the display window.
    pygame.init()

    width = 640
    height = 480
    my_win = pygame.display.set_mode((width, height))

    # Initialize ball
    x = random.randint(0,width)
    y = random.randint(0,height)
    radius = 10
    color = pygame.color.Color("Red")
    increment = 1


    # The game loop starts here.
    keep_going = True
    while (keep_going):

        # 1. Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False


        # 2. Apply rules of game world
        # None currently

        # 3. Simulate the world
        # None currently

        # 4. Draw frame
        # Draw Background
        my_win.fill(pygame.color.Color("black"))

        # Draw ball
        pygame.draw.circle(my_win, color, (x, y), radius)
        x += increment
        if x + radius == width or x - radius == 0:
            color = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
            increment *= -1


        # Swap display
        pygame.display.update()

    # The game loop ends here.

    pygame.quit()


# Start game
run_game()