#
# Author: Caleb L'Italien
#
# Plays a two-player breakout against an AI, has 5 levels of increased difficulty.
#
import os
import pygame
import random
import math
from moving_ball_sprite_2d import *
from paddle_sprite_2d import *
from paddle_ai import *
from background import *

MAX_BRICKS_IN_LAYER = 20
BRICK_STARTING_X = 10
BRICK_STARTING_Y = 200
DEFAULT_X_SPEED = 1.5
DEFAULT_Y_SPEED = 1.5
BRICK_WIDTH = 30
BRICK_HEIGHT = 20
PADDLE_SPEED = 5
WIDTH = 640
HEIGHT = 750
POINTS_PER_BRICK = 1
POINTS_PER_LOST_LIFE = 15
POINTS_PER_LEVEL_CHANGE = 10
BRICK_PROBABILITY = 7
MAX_LEVELS = 5
PADDLE_Y_BUFFER = 45
SIDE_BUFFER = 10
PADDLE_WIDTH_GOD_MODE = WIDTH - 40
COST_FOR_LIFE = 50

WIN = "WIN"
LOSS = "LOSE"
BALL_COLORS = ["aquamarine3","aquamarine4","blueviolet","brown3","cadetblue","chartreuse3","crimson",
                   "cyan3","darkolivegreen3","darkolivegreen4","darkorchid2","darkorchid3","darkorchid4","darkseagreen4",
                   "darkturquoise","deeppink3","deeppink4","goldenrod3","hotpink3","hotpink4","indianred",
                   "indianred4","magenta","magenta3","magenta4","maroon","mediumorchid3","mediumorchid4","mediumpurple",
                   "mediumpurple3","mediumpurple4","mediumslateblue","olive","olivedrab","olivedrab4"]

def run_game():
    pygame.init()

    pygame.mixer.init()
    s = 'Sounds'
    bonk = pygame.mixer.Sound(os.path.join(s, 'bonk.ogg'))
    ding = pygame.mixer.Sound(os.path.join(s, 'ding.ogg'))
    fail = pygame.mixer.Sound(os.path.join(s, 'fail.ogg'))
    shuffle = pygame.mixer.Sound(os.path.join(s, 'screech.ogg'))
    startingShot = pygame.mixer.Sound(os.path.join(s, 'startingShot.ogg'))
    infinite = pygame.mixer.Sound(os.path.join(s, 'teleport.ogg'))
    speedUp = pygame.mixer.Sound(os.path.join(s, 'valorant-teleporter.ogg'))
    victory = pygame.mixer.Sound(os.path.join(s, 'victory.ogg'))
    music = pygame.mixer.music.load(os.path.join(s, 'elevator.ogg'))
    pygame.mixer.music.play(-1)

    borders = []

    my_win = pygame.display.set_mode((WIDTH, HEIGHT))

    ball_color_beginning = BALL_COLORS[random.randint(0, len(BALL_COLORS) - 1)]

    paddle_width = 120
    paddle_height = 10
    border_color = "antiquewhite"

    paddle = Paddle(280, HEIGHT - PADDLE_Y_BUFFER, 10000, pygame.color.Color(border_color), paddle_width, paddle_height)
    paddleAI = Paddle_AI(280, 40, 10000, pygame.color.Color(border_color), paddle_width, paddle_height)

    ball = __create_ball(ball_color_beginning)

    border_left = Brick(2, 2, 10000, border_color, 2, HEIGHT - 5, True)
    border_right = Brick(WIDTH - 4, 2, 10000, border_color, 2, HEIGHT - 5, True)
    border_top = Brick(2, 2, 10000, border_color, WIDTH - 4, 2, True)
    border_bottom = Brick(2, HEIGHT - 5, 10000, border_color, WIDTH - 2, 2, True)

    borders.append(border_left)
    borders.append(border_right)
    borders.append(border_top)
    borders.append(border_bottom)

    dt = 0

    level = 1
    lives = 3

    starting = True
    keepGoing = True
    level_change = False
    points = 0

    bricks = __create_bricks(level)
    BackGround = Background('Background.png', [0,0])

    while (keepGoing):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        my_win.fill(pygame.color.Color("black"))
        my_win.blit(BackGround.image, BackGround.rect)

        if starting:
            __get_ready(my_win)
            starting = False
            pygame.time.delay(4000)
            pygame.mixer.Sound.play(startingShot)

        paddleAI.simulate_play(ball, level, paddle)

        font = pygame.font.Font('game of squids.ttf', 26)
        level_render = font.render("Level: " + str(level), True, "antiquewhite")
        score_render = font.render("Score: " + str(points), True, "antiquewhite")

        ball_color = BALL_COLORS[random.randint(0, len(BALL_COLORS) - 1)]

        if keepGoing:
            for border in borders:
                border.draw(my_win)

        if level_change:
            bricks = __create_bricks(level)
            level_change = False
            paddle_x = paddle.position_x()
            paddle = Paddle(paddle_x, HEIGHT - PADDLE_Y_BUFFER, 10000, pygame.color.Color("antiquewhite"), paddle_width, paddle_height)

        ball.simulate(dt, WIDTH, HEIGHT)
        
        collision_paddle = ball.collideRect(paddle)
        collision_paddleAI = ball.collideRect(paddleAI)

        if collision_paddle is not None:
            ball_x, ball_y = ball.getPosition()
            ball_vx, ball_vy = ball.getVelocity()
            ball = MovingBall(ball_x, ball_y, 10, 10, pygame.color.Color(ball_color), ball_vx, ball_vy)
            ball.speedUp()
        
        if collision_paddleAI is not None:
            ball_x, ball_y = ball.getPosition()
            ball_vx, ball_vy = ball.getVelocity()
            ball = MovingBall(ball_x, ball_y, 10, 10, pygame.color.Color(ball_color), ball_vx, ball_vy)
            ball.slowDown()

        if keepGoing:
            for brick_layer in bricks:
                for brick in brick_layer:
                    brick.draw(my_win)
                    collision_brick = ball.collideRect(brick)

                    if collision_brick is not None:
                        if brick.isInvincible() is False:
                            pygame.mixer.Sound.play(ding)
                            brick_layer.remove(brick)

                            brick_x, brick_y = brick.getRect_p().x, brick.getRect_p().y
                            color = brick.getColor()
                            new_brick = __create_new_brick(brick_x, color, __getNewBrickPosition(brick_y))

                            if new_brick is not None:
                                brick_layer.append(new_brick)

                            points += POINTS_PER_BRICK

                        else:
                            pygame.mixer.Sound.play(bonk)
                            points -= POINTS_PER_BRICK

                        ball_x, ball_y = ball.getPosition()
                        ball_vx, ball_vy = ball.getVelocity()
                        ball = MovingBall(ball_x, ball_y, 10, 10, pygame.color.Color(ball_color), ball_vx, ball_vy)
                        ball.speedUp()

        lives_left, lives_x = __render_lives(lives, font)

        if ball.topSpeeds():
            paddle_x = paddle.position_x()
            if paddle_width != PADDLE_WIDTH_GOD_MODE:
                paddle = Paddle(paddle_x, HEIGHT - PADDLE_Y_BUFFER, 10000, pygame.color.Color("antiquewhite"),
                                paddle_width + 40, paddle_height)

        if ball.hit_bottom(HEIGHT):
            points -= POINTS_PER_LOST_LIFE
            lives -= 1
            if lives == 0:
                keepGoing = False
                __game_over(my_win, LOSS, fail)
                pygame.time.delay(2000)
            else:
                ball.resetSpeed()

                paddle_x = paddle.position_x()
                paddle = Paddle(paddle_x, HEIGHT - PADDLE_Y_BUFFER, 10000, pygame.color.Color("antiquewhite"), paddle_width, paddle_height)
                pygame.time.delay(1000)

        if ball.hit_top():
            points += POINTS_PER_LEVEL_CHANGE + (level * 5)

            if level == MAX_LEVELS:
                keepGoing = False
                __game_over(my_win, WIN, victory)
                pygame.time.delay(2000)
            else:
                level += 1
                ball.resetSpeed()
                level_change = True

                paddle_x = paddle.position_x()
                paddle = Paddle(paddle_x, HEIGHT - PADDLE_Y_BUFFER, 10000, pygame.color.Color("antiquewhite"), paddle_width, paddle_height)
                pygame.time.delay(1000)

        paddle.draw(my_win)
        paddleAI.draw(my_win)
        ball.draw(my_win)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.moveLeft(PADDLE_SPEED)

        if keys[pygame.K_RIGHT]:
            paddle.moveRight(PADDLE_SPEED)

        if keys[pygame.K_b]:
            ball.speedUp()
            pygame.mixer.Sound.play(speedUp)

        if keys[pygame.K_g]:
            if lives != math.inf:
                pygame.mixer.Sound.play(infinite)
            lives = math.inf

            paddle_x = SIDE_BUFFER
            paddle_width = WIDTH - 40
            paddle = Paddle(paddle_x, HEIGHT - PADDLE_Y_BUFFER, 10000, pygame.color.Color("antiquewhite"), paddle_width, paddle_height)

        if keys[pygame.K_s]:
            pygame.mixer.Sound.play(shuffle)
            level_change = True

        if keys[pygame.K_t]:
            if points >= COST_FOR_LIFE:
                points -= COST_FOR_LIFE
                lives += 1

        my_win.blit(level_render, (10, 5))
        my_win.blit(lives_left, (lives_x, 5))
        my_win.blit(score_render, (10, HEIGHT - 38))

        pygame.display.update()

        if keys[pygame.K_q]:
            keepGoing = False
            pygame.quit()

    pygame.time.delay(2000)
    pygame.quit()


def __create_brick_layer(layer, color, level):
    bricks = []
    tries = 0
    while tries < MAX_BRICKS_IN_LAYER:
        brick_probability = random.randint(1,10)
        successful_range = 1 + level

        if brick_probability <= successful_range:
            brick_x = BRICK_STARTING_X + 31 * tries
            brick_y = BRICK_STARTING_Y + 25 * layer
            bricks.append(Brick(brick_x, brick_y, 10, pygame.color.Color(color), BRICK_WIDTH, BRICK_HEIGHT, False))

        tries += 1
    return bricks


def __create_bricks(level):
    bricks = []
    brick_layer_one = __create_brick_layer(0, "cadetblue3", level)
    brick_layer_two = __create_brick_layer(1, "darkolivegreen", level)
    brick_layer_three = __create_brick_layer(2, "darkolivegreen3", level)
    brick_layer_four = __create_brick_layer(3, "burlywood2", level)
    brick_layer_five = __create_brick_layer(4, "burlywood4", level)

    bricks.append(brick_layer_one)
    bricks.append(brick_layer_two)
    bricks.append(brick_layer_three)
    bricks.append(brick_layer_four)
    bricks.append(brick_layer_five)

    return bricks


def __create_new_brick(brick_x, color, position):
    brick_chance = random.randint(1,10)
    brick_invincibility_chance = random.randint(1,3)

    if brick_chance <= BRICK_PROBABILITY:
        brick_invincibility = False
        if brick_invincibility_chance == 1:
            brick_invincibility = True
            color = "antiquewhite"
        return Brick(brick_x, position, 10, pygame.color.Color(color), BRICK_WIDTH, BRICK_HEIGHT, brick_invincibility)
    return None


def __render_lives(lives, font):
    if lives != 1 and lives != math.inf:
        lives_left = font.render("Lives: 00" + str(lives), True, "white")
        lives_x = 450
    elif lives == math.inf:
        lives_left = font.render("Lives: " + str(lives), True, "white")
        lives_x = 470
    else:
        lives_left = font.render("LAST LIFE", True, "crimson")
        lives_x = 472
    return lives_left, lives_x


def __game_over(window, win_status, sound):
    if win_status == "WIN":
        border_color = "darkseagreen4"
    else:
        border_color = "crimson"
    pygame.mixer.Sound.play(sound)

    font = pygame.font.Font('game of squids.ttf', 32)
    game_over = font.render("GAME OVER", True, border_color)
    game_conclusion = font.render("YOU " + str(win_status), True, border_color)

    borders = []
    border_left = Brick(2, 2, 10000, border_color, 2, HEIGHT - 5, True)
    border_right = Brick(WIDTH - 4, 2, 10000, border_color, 2, HEIGHT - 5, True)
    border_top = Brick(2, 2, 10000, border_color, WIDTH - 4, 2, True)
    border_bottom = Brick(2, HEIGHT - 5, 10000, border_color, WIDTH - 2, 2, True)

    borders.append(border_left)
    borders.append(border_right)
    borders.append(border_top)
    borders.append(border_bottom)

    for border in borders:
        border.draw(window)

    game_over_size_x, y = game_over.get_size()
    game_conclusion_size_x, y = game_conclusion.get_size()

    game_over_location = WIDTH / 2 - game_over_size_x / 2
    game_conclusion_location = WIDTH / 2 - game_conclusion_size_x / 2

    window.blit(game_over, (game_over_location, HEIGHT / 2))
    window.blit(game_conclusion, (game_conclusion_location, (HEIGHT / 2) + 40))


def __get_ready(window):
    pygame.time.delay(1000)
    font = pygame.font.Font('game of squids.ttf', 32)
    smallerFont = pygame.font.Font('game of squids.ttf', 18)

    get_ready = font.render("GET READY", True, "antiquewhite")
    speed_up_render = smallerFont.render("Press 'b' to speed up", True, "antiquewhite")
    god_mode_render = smallerFont.render("Press 'g' to enter god mode", True, "antiquewhite")
    shuffle_bricks_render = smallerFont.render("Press 's' to shuffle bricks", True, "antiquewhite")
    trade_for_life_render = smallerFont.render("Press 't' to trade in 50 points for a life", True, "antiquewhite")
    quit_game_render = smallerFont.render("Press 'q' to quit", True, "antiquewhite")

    get_ready_size_x, y = get_ready.get_size()
    speed_up_size_x, y = speed_up_render.get_size()
    god_mode_size_x, y = god_mode_render.get_size()
    shuffle_bricks_size_x, y = shuffle_bricks_render.get_size()
    trade_for_life_size_x, y = trade_for_life_render.get_size()
    quit_game_size_x, y = quit_game_render.get_size()

    get_ready_x = WIDTH / 2 - get_ready_size_x / 2
    speed_up_x = WIDTH / 2 - speed_up_size_x / 2
    god_mode_x = WIDTH / 2 - god_mode_size_x / 2
    shuffle_bricks_x = WIDTH / 2 - shuffle_bricks_size_x / 2
    trade_for_life_x = WIDTH / 2 - trade_for_life_size_x / 2
    quit_game_x = WIDTH / 2 - quit_game_size_x / 2

    window.blit(get_ready, (get_ready_x, HEIGHT / 2))

    window.blit(speed_up_render, (speed_up_x, HEIGHT/2 + 50))
    window.blit(god_mode_render, (god_mode_x, HEIGHT/2 + 80))
    window.blit(shuffle_bricks_render, (shuffle_bricks_x, HEIGHT/2 + 110))
    window.blit(trade_for_life_render, (trade_for_life_x, HEIGHT/2 + 140))
    window.blit(quit_game_render, (quit_game_x, (HEIGHT/2 + 170)))

    pygame.display.update()
    

def __create_ball(color):
    ball_starting_x = random.randint(0,WIDTH)
    ball_x_direction_multiplier = random.randint(1,2)

    if ball_x_direction_multiplier == 2:
        ball_x_direction_multiplier = -1

    ball = MovingBall(ball_starting_x, 375, 10, 10, pygame.color.Color(color), DEFAULT_X_SPEED *
                      ball_x_direction_multiplier, DEFAULT_Y_SPEED)
    return ball


def __getNewBrickPosition(position):
    position = position + 100
    if position > HEIGHT - 200:
        position = HEIGHT - 200
    return position
    

if __name__ == "__main__":
    run_game()