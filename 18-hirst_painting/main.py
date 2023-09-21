###This code will not work in repl.it as there is no access to the colorgram package here.###
##We talk about this in the video tutorials##
# import colorgram
#
# rgb_colors = []
# colors = colorgram.extract('image.jpg', 30)
# for color in colors:
#     r = color.rgb.r
#     g = color.rgb.g
#     b = color.rgb.b
#     new_color = (r ,g, b)
#     rgb_colors.append(new_color)
# print(rgb_colors)


import turtle
from turtle import Turtle, Screen
import random


color_list = [(202, 164, 110), (149, 75, 50), (222, 201, 136), (53, 93, 123), (170, 154, 41), (138, 31, 20), (134, 163, 184), (197, 92, 73), (47, 121, 86), (73, 43, 35), (145, 178, 149), (14, 98, 70), (232, 176, 165), (160, 142, 158), (54, 45, 50), (101, 75, 77), (183, 205, 171), (36, 60, 74), (19, 86, 89), (82, 148, 129), (147, 17, 19), (27, 68, 102), (12, 70, 64), (107, 127, 153), (176, 192, 208), (168, 99, 102)]

ger = Turtle()
screen = Screen()


ger.shape("arrow")
ger.speed("fastest")
ger.penup()
initial_x = -screen.window_width() / 2
initial_y = -screen.window_height() / 2
ger.setpos(initial_x, initial_y)
ger.setheading(0)
turtle.colormode(255)
ger.hideturtle()

for _ in range(10):
    for _ in range(10):
        ger.setheading(0)
        ger.dot(20, random.choice(color_list))
        ger.forward(50)
    ger.setheading(180)
    ger.forward(500)
    ger.setheading(90)
    ger.forward(50)


screen.exitonclick()