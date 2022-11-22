"""
Derived from code provided at
http://programarcadegames.com/
"""
import pygame


from spritesheet_functions import SpriteSheet
from vector import Vector

JUMP_HEIGHT = 10
GRAVITY = 0.25
WINDOW_HEIGHT = 480

class Player(pygame.sprite.Sprite):

    # -- Attributes
    # Set speed vector of player

    # This holds all the images for the animated walk left/right
    # of our player
    walking_right = []
    walking_left = []


    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.v = Vector(0,0)

        sprite_sheet = SpriteSheet("p1_walk.png")
        # Load all the images into a list
        image = sprite_sheet.get_image(0, 0, 66, 90)
        self.walking_right.append(image)
        image_flipped = pygame.transform.flip(image, True, False)
        self.walking_left.append(image_flipped)

        image = sprite_sheet.get_image(66, 0, 66, 90)
        self.walking_right.append(image)
        image_flipped = pygame.transform.flip(image, True, False)
        self.walking_left.append(image_flipped)

        image = sprite_sheet.get_image(132, 0, 67, 90)
        self.walking_right.append(image)
        image_flipped = pygame.transform.flip(image, True, False)
        self.walking_left.append(image_flipped)

        image = sprite_sheet.get_image(0, 93, 66, 90)
        self.walking_right.append(image)
        image_flipped = pygame.transform.flip(image, True, False)
        self.walking_left.append(image_flipped)

        image = sprite_sheet.get_image(66, 93, 66, 90)
        self.walking_right.append(image)
        image_flipped = pygame.transform.flip(image, True, False)
        self.walking_left.append(image_flipped)

        image = sprite_sheet.get_image(132, 93, 72, 90)
        self.walking_right.append(image)
        image_flipped = pygame.transform.flip(image, True, False)
        self.walking_left.append(image_flipped)

        image = sprite_sheet.get_image(0, 186, 70, 90)
        self.walking_right.append(image)
        image_flipped = pygame.transform.flip(image, True, False)
        self.walking_left.append(image_flipped)

        # Set the image the player starts with
        self.image = self.walking_right[0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        self.direction = "right"

    def update(self):
        """ Move the player. """
        # Gravity etc
        self.simulate()

        # Move left/right
        if self.direction == "right":
            frame = (self.rect.x // 30) % len(self.walking_right)
            self.image = self.walking_right[frame]
        if self.direction == "left":
            frame = (self.rect.x // 30) % len(self.walking_left)
            self.image = self.walking_left[frame]


    def simulate(self):
        """ Calculate effect of gravity. """
        ## NOTE USE self.rect for position
        self.rect.x += self.v.x
        self.rect.y += self.v.y

    def jump(self):
        """ Called when user hits 'jump' button. """
        self.v.y = self.v.y - JUMP_HEIGHT

    def gravity(self):
        if self.rect.y < (WINDOW_HEIGHT - self.rect.height):
            self.v.y = self.v.y + GRAVITY
        else:
            self.rect.y = WINDOW_HEIGHT - self.rect.height

    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.direction = "left"
        self.v.x = self.v.x - 3

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.direction = "right"
        self.v.x = self.v.x + 3

    def stopX(self):
        """ Called when the user lets off the keyboard. """
        self.v.x = 0

    def stopY(self):
        self.v.y = 0

if __name__ == "__main__":
    size = (640,480)
    screen = pygame.display.set_mode(size)
    p = Player()