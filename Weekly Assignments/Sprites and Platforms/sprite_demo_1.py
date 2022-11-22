"""

Author: John Rieffel

Based off of 

Simpson College Computer Science Material

Game art from Kenney.nl:
http://opengameart.org/content/platformer-art-deluxe

"""

import pygame

from player import Player
from simple_platform import Box

def main():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    HEIGHT = 480
    WIDTH = 640
    size = [WIDTH,HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("demo with sprite sheets")

    active_sprite_list = pygame.sprite.Group()
    platforms = []
    # Create the player
    player = Player()
    platform = Box(pygame.color.Color("darkolivegreen3"), 50, 50)
    platform_two = Box(pygame.color.Color("darkgoldenrod3"),50,50)
    platform_three = Box(pygame.color.Color("darkmagenta"), 50, 50)
    platform_four = Box(pygame.color.Color("crimson"), 50, 50)
    platform_five = Box(pygame.color.Color("yellow"), 50, 50)

    platform.rect.x = 250
    platform_two.rect.x = 500
    platform_three.rect.x = 1
    platform_four.rect.x = 100
    platform_five.rect.x = 100

    platform.rect.y = HEIGHT - platform.rect.h
    platform_two.rect.y = HEIGHT - platform.rect.h
    platform_three.rect.y = HEIGHT / 2
    platform_four.rect.y = HEIGHT / 4
    platform_five.rect.y = HEIGHT - 100

    platforms.append(platform)
    platforms.append(platform_two)
    platforms.append(platform_three)
    platforms.append(platform_four)
    platforms.append(platform_five)

    # Create all the levels

    player.rect.x = 100 
    player.rect.y = HEIGHT - player.rect.height
    active_sprite_list.add(player,platform, platform_two, platform_three, platform_four, platform_five)

    #Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        player.gravity()
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

            player.simulate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.stopX()
                if event.key == pygame.K_RIGHT:
                    player.stopX()

        # Update the player.
        active_sprite_list.update()

        for platform in platforms:
            if pygame.sprite.collide_rect(player, platform):
                distance_x = abs(player.rect.x - platform.rect.x)
                distance_y = abs(player.rect.y - platform.rect.y)
                if distance_x <= player.rect.width:
                    player.stopX()
                if distance_y <= player.rect.height:
                    player.stopY()

        screen.fill(pygame.color.Color("gray14")) 
        active_sprite_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

if __name__ == "__main__":
    main()
