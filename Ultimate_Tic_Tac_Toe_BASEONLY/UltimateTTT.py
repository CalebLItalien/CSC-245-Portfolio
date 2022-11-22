import pygame
from rect_2d import *

WIDTH = 700
HEIGHT = 700

def run_game():
    pygame.init()

    borders = []

    my_win = pygame.display.set_mode((WIDTH, HEIGHT))
    border_color = "antiquewhite"

    border_left = Rectangle(2, 2, 10000, border_color, 2, HEIGHT - 5)
    border_right = Rectangle(WIDTH - 4, 2, 10000, border_color, 2, HEIGHT - 5)
    border_top = Rectangle(2, 2, 10000, border_color, WIDTH - 4, 2)
    border_bottom = Rectangle(2, HEIGHT - 5, 10000, border_color, WIDTH - 2, 2)

    borders.append(border_left)
    borders.append(border_right)
    borders.append(border_top)
    borders.append(border_bottom)

    dt = 0
    
    keepGoing = True

    while (keepGoing):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        my_win.fill(pygame.color.Color("black"))

        if keepGoing:
            for border in borders:
                border.draw(my_win)

        pygame.display.update()
    pygame.time.delay(1500)
    pygame.quit()

if __name__ == "__main__":
    run_game()
