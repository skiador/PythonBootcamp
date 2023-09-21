from turtle import Screen
from ball import Ball
from paddle import Paddle
from scoreboard import ScoreBoard
import time

screen = Screen()
screen.screensize(canvwidth=800, canvheight=600)
screen.bgcolor("black")
screen.title("Pong")

r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()
scoreboard = ScoreBoard()

screen.listen()
screen.onkeypress(r_paddle.move_up, "Up")
screen.onkeypress(r_paddle.move_down, "Down")
screen.onkeypress(l_paddle.move_up, "w")
screen.onkeypress(l_paddle.move_down, "s")

sleep = 0.1
game_is_on = True
while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    # Collision detection top and bottom
    if ball.ycor() > 285 or ball.ycor() < -285:
        ball.bounce_y()

    # Detect collision with paddles
    elif (ball.xcor() > 330 and ball.distance(r_paddle) <= 50) or (ball.xcor() < -330 and ball.distance(l_paddle) <= 50):
        ball.bounce_x()

    # Detect ball out of bounds on the left
    if ball.xcor() <= -350:
        ball.reset_position()
        scoreboard.r_point()

    # Detect ball out of bounds on the right
    if ball.xcor() >= 350:
        ball.reset_position()
        scoreboard.l_point()



screen.exitonclick()