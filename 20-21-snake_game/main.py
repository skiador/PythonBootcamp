from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time


SPEED = 0.05

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(screen.bye, "Escape")


game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(SPEED)
    snake.move()
    scoreboard.update_score()

    # Detect food collision
    if snake.head.distance(food) < 15:
        food.refresh_location()
        scoreboard.increase_score()
        scoreboard.update_score()
        snake.extend()

    if not (-290 < snake.head.xcor() < 290 and -290 < snake.head.ycor() < 290):
        scoreboard.reset_score()
        snake.reset_snake()

    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            scoreboard.reset_score()
            snake.reset_snake()

screen.exitonclick()



