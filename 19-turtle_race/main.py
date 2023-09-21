from turtle import Turtle, Screen
import random
import numpy as np

COLOR_LIST = ["red", "orange", "yellow", "green", "lightblue", "blue", "violet", "pink"]
SCREEN_HEIGHT = 400
SCREEN_WIDTH = 500


def random_movement(turtle):
    amount = np.random.normal(5, 5)
    turtle.forward(amount)
    # if turtle.color()[0] == "orange":
    #     turtle.forward(amount)


screen = Screen()
screen.screensize(SCREEN_WIDTH, SCREEN_HEIGHT)
# Ask for a winner
user_winner = screen.textinput("Bets", prompt=f"Which turtle will win? {COLOR_LIST}")

turtle_list = {}
for index, color in enumerate(COLOR_LIST):
    turtle_list[color] = Turtle()
    turtle_list[color].shape("turtle")
    turtle_list[color].color(color)
    turtle_list[color].speed(0)
    turtle_list[color].penup()
    turtle_list[color].setpos(-SCREEN_WIDTH/2, 150-index*300/len(COLOR_LIST))

ref = Turtle()
ref.color("black")
ref.shape("turtle")
ref.speed(0)
ref.penup()
ref.setpos(250, -200)
ref.pendown()
ref.setpos(250, 200)
ref.penup()
ref.setpos(0, -200)
ref.setheading(90)

finish = False
while not finish:
    for turtle in turtle_list.values():
        random_movement(turtle)
        if turtle.xcor() >= 250:
            finish = True
            winner_turtle = turtle


ref.write(f"{winner_turtle.color()[0]} wins!", move=True, font=('Arial', 15, 'normal'))

if winner_turtle.color()[0] == user_winner:
    print("You win! Your turtle won!")
else:
    print(f"You bet for {user_winner}... The winner is {winner_turtle.color()[0]}")




screen.exitonclick()











