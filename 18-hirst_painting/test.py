import turtle
from turtle import Turtle, Screen
import random


ANGLES = [0, 90, 180, 270]


def random_color():
    r = random.random()
    g = random.random()
    b = random.random()
    return (r, g, b)


ger = Turtle()
screen = Screen()

ger.shape("arrow")
ger.color("blue")
ger.speed(0)
ger.pensize(1)
ger.setheading(0)


while True:
    ger.circle(100)
    ger.pencolor(random_color())
    ger.setheading(ger.heading() + 16.578)







screen.exitonclick()

