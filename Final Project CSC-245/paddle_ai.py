from paddle_sprite_2d import *
from rect_2d import *
import random

SIDE_BUFFER = 10
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
PADDLE_SPEED = 4
AI_NERF = 2


class Paddle_AI(Paddle):
    def __init__(self, x, y, m, color, width, height):
        Brick.__init__(self, x, y, m, color, width, height, True)
        Paddle.__init__(self, x, y, m, color, width, height)

    def simulate_play(self, ball, level, paddle):
        if self.__on_AI_side(ball):
            successful_decision = self.__successful_decision()
            distance_x = ball.p.x - (self.p.x + self.width/2)

            if successful_decision:
                if distance_x < 0:
                    self.moveLeft(PADDLE_SPEED + level)
                if distance_x > 0 + self.width/2:
                    self.moveRight(PADDLE_SPEED + level)
            else:
                if distance_x < 0:
                    self.moveRight(PADDLE_SPEED + level)
                if distance_x > 0 + self.width/2:
                    self.moveLeft(PADDLE_SPEED + level)
        else:
            self.__mimic(paddle, level)


    def __on_AI_side(self, ball):
        return ball.p.y <= WINDOW_HEIGHT * (2/3)
            

    def __successful_decision(self):
        decision = random.randint(1,10)
        return decision > AI_NERF

    def __mimic(self, paddle, level):
        distance_x = self.p.x - paddle.p.x
        if distance_x < 0:
            self.moveRight(level)
        elif distance_x > 0:
            self.moveLeft(level)