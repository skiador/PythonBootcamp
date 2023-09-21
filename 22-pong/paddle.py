import turtle
from turtle import Turtle

PLAYER_LENGTH = 100
PLAYER_WIDTH = 20
PLAYER_MOVEMENT = 50


class Paddle(Turtle):

    def __init__(self, coordinates):
        super().__init__()
        self.hideturtle()
        self.shape("square")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.color("white")
        self.speed(0)
        self.penup()
        self.goto(coordinates)
        self.showturtle()

    def move_up(self):
        if self.ycor() >= 300-self.shapesize()[1]:
            pass
        else:
            self.sety(self.ycor() + PLAYER_MOVEMENT)

    def move_down(self):
        if self.ycor() <= -300 + self.shapesize()[1]:
            pass
        else:
            self.sety(self.ycor() - PLAYER_MOVEMENT)
