##
## Author: Caleb L'Italien
##
## 09.28.22
##
## Plays a version of the classic atari game breakout.
##
import pygame
import random
from moving_ball_sprite_2d import *
from paddle_sprite_2d import *

BRICKS_IN_LAYER = 20
BRICKS_IN_SUN = 6
SUN_LAYER = -1
SUN_STARTING_X = 227
BRICK_STARTING_X = 10
BRICK_STARTING_Y = 45
DEFAULT_X_SPEED = 1.5
DEFAULT_Y_SPEED = 1.5
BRICK_WIDTH = 30
BRICK_HEIGHT = 20
PADDLE_SPEED = 5
WIDTH = 640
HEIGHT = 700
BALL_COLORS = ["aquamarine3","aquamarine4","blueviolet","brown3","cadetblue","chartreuse3","crimson",
                   "cyan3","darkolivegreen3","darkolivegreen4","darkorchid2","darkorchid3","darkorchid4","darkseagreen4",
                   "darkturquoise","deeppink3","deeppink4","goldenrod3","hotpink3","hotpink4","indianred",
                   "indianred4","magenta","magenta3","magenta4","maroon","mediumorchid3","mediumorchid4","mediumpurple",
                   "mediumpurple3","mediumpurple4","mediumslateblue","olive","olivedrab","olivedrab4"]

def run_game():
    pygame.init()

    bricks = []
    borders = []

    my_win = pygame.display.set_mode((WIDTH, HEIGHT))

    ball_color_beginning = BALL_COLORS[random.randint(0, len(BALL_COLORS) - 1)]

    paddle_width = 95
    paddle_height = 10
    border_color = "antiquewhite"

    paddle = Paddle(280, HEIGHT - 40, 10000, pygame.color.Color(border_color), paddle_width, paddle_height)
    ball = __create_ball(ball_color_beginning)

    border_left = Rectangle(2, 2, 10000, border_color, 2, HEIGHT - 5)
    border_right = Rectangle(WIDTH - 4, 2, 10000, border_color, 2, HEIGHT - 5)
    border_top = Rectangle(2, 2, 10000, border_color, WIDTH - 4, 2)
    border_bottom = Rectangle(2, HEIGHT - 5, 10000, border_color, WIDTH - 2, 2)

    brick_layer_one = __create_bricks(0, "cadetblue3")
    brick_layer_two = __create_bricks(1, "darkolivegreen")
    brick_layer_three = __create_bricks(2, "darkolivegreen3")
    brick_layer_four = __create_bricks(3, "burlywood2")
    brick_layer_five = __create_bricks(4,"darkgoldenrod4")
    sun_layer = __create_bricks(-1, "darkgoldenrod1")

    bricks.append(brick_layer_one)
    bricks.append(brick_layer_two)
    bricks.append(brick_layer_three)
    bricks.append(brick_layer_four)
    bricks.append(brick_layer_five)
    bricks.append(sun_layer)

    borders.append(border_left)
    borders.append(border_right)
    borders.append(border_top)
    borders.append(border_bottom)

    dt = 0

    points = 0
    lives = 3
    win = "WIN"
    loss = "LOSE"

    starting = True
    keepGoing = True

    while (keepGoing):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        my_win.fill(pygame.color.Color("black"))

        ball_color = BALL_COLORS[random.randint(0, len(BALL_COLORS) - 1)]

        if starting:
            __get_ready(my_win)
            starting = False
            pygame.time.delay(1500)

        ball.simulate(dt, WIDTH, HEIGHT)

        if len(bricks) == 0 or lives == 0:
            if lives > 0:
                __game_over(my_win, win)
            else:
                __game_over(my_win, loss)
            keepGoing = False

        for brick_layer in bricks:
            for brick in brick_layer:
                brick.draw(my_win)

        collision_paddle = ball.collideRect(paddle)
        if collision_paddle is not None:
            ball_x, ball_y = ball.getPosition()
            ball_vx, ball_vy = ball.getVelocity()
            ball = MovingBall(ball_x, ball_y, 10, 10, pygame.color.Color(ball_color), ball_vx, ball_vy)

        for brick_layer in bricks:
            for brick in brick_layer:
                collision_brick = ball.collideRect(brick)
                if collision_brick is not None:
                    brick_layer.remove(brick)
                    ball.speedUp()
                    ball_x, ball_y = ball.getPosition()
                    ball_vx, ball_vy = ball.getVelocity()
                    ball = MovingBall(ball_x, ball_y, 10, 10, pygame.color.Color(ball_color), ball_vx, ball_vy)

                    points += 1

                if len(brick_layer) == 0:
                    bricks.remove(brick_layer)

        font = pygame.font.Font('game of squids.ttf', 26)
        score = font.render("Score: " + str(points), True, "white")
        if lives != 1:
            lives_left = font.render("Lives: " + str(lives), True, "white")
            lives_x = 488
        else:
            lives_left = font.render("LAST LIFE", True, "red")
            lives_x = 472

        if ball.hit_bottom(HEIGHT):
            lives -= 1
            ball.resetSpeed()
            pygame.time.delay(1000)

        if ball.topSpeeds():
            paddle_x = paddle.position_x()
            paddle = Paddle(paddle_x, HEIGHT - 40, 10000, pygame.color.Color("antiquewhite"), paddle_width + 40, paddle_height)
        else:
            paddle_x = paddle.position_x()
            paddle = Paddle(paddle_x, HEIGHT - 40, 10000, pygame.color.Color("antiquewhite"), paddle_width, paddle_height)

        if keepGoing:
            for border in borders:
                border.draw(my_win)

        paddle.draw(my_win)
        ball.draw(my_win)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.moveLeft(PADDLE_SPEED)

        if keys[pygame.K_RIGHT]:
            paddle.moveRight(PADDLE_SPEED)

        my_win.blit(score, (10, 5))
        my_win.blit(lives_left, (lives_x, 5))

        pygame.display.update()
    pygame.time.delay(1500)
    pygame.quit()


def __create_bricks(layer, color):
    bricks = []
    num_bricks = 0

    if layer == SUN_LAYER:
        while num_bricks < BRICKS_IN_SUN:
            brick_x = SUN_STARTING_X + 31 * num_bricks
            brick_y = BRICK_STARTING_Y + 25 * layer

            bricks.append(Rectangle(brick_x, brick_y, 10, pygame.color.Color(color), BRICK_WIDTH, BRICK_HEIGHT))
            num_bricks += 1
    else:
        while num_bricks < BRICKS_IN_LAYER:
            brick_x = BRICK_STARTING_X + 31 * num_bricks
            brick_y = BRICK_STARTING_Y + 25 * layer

            bricks.append(Rectangle(brick_x, brick_y, 10, pygame.color.Color(color), BRICK_WIDTH, BRICK_HEIGHT))
            num_bricks += 1
    return bricks


def __game_over(window, win_status):
    if win_status == "WIN":
        border_color = "darkseagreen4"
        spacing = " "
    else:
        border_color = "crimson"
        spacing = ""

    font = pygame.font.Font('game of squids.ttf', 32)
    game_over = font.render("GAME OVER", True, "antiquewhite")
    game_conclusion = font.render(spacing + "YOU " +  str(win_status), True, "antiquewhite")

    borders = []
    border_left = Rectangle(2, 2, 10000, border_color, 2, HEIGHT - 5)
    border_right = Rectangle(WIDTH - 4, 2, 10000, border_color, 2, HEIGHT - 5)
    border_top = Rectangle(2, 2, 10000, border_color, WIDTH - 4, 2)
    border_bottom = Rectangle(2, HEIGHT - 5, 10000, border_color, WIDTH - 2, 2)

    borders.append(border_left)
    borders.append(border_right)
    borders.append(border_top)
    borders.append(border_bottom)

    for border in borders:
        border.draw(window)

    window.blit(game_over, (230, HEIGHT / 2))
    window.blit(game_conclusion, (245, (HEIGHT / 2) + 40))
    pygame.display.update()


def __get_ready(window):
    font = pygame.font.Font('game of squids.ttf', 32)
    get_ready = font.render("GET READY", True, "antiquewhite")

    window.blit(get_ready, (230, HEIGHT / 2))
    pygame.display.update()
    

def __create_ball(color):
    ball_starting_x = random.randint(0,WIDTH)
    ball_x_direction_multiplier = random.randint(1,2)

    if ball_x_direction_multiplier == 2:
        ball_x_direction_multiplier = -1

    ball = MovingBall(ball_starting_x, 200, 10, 10, pygame.color.Color(color), DEFAULT_X_SPEED *
                      ball_x_direction_multiplier, DEFAULT_Y_SPEED)
    return ball
    
if __name__ == "__main__":
    run_game()
