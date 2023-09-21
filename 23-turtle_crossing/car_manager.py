from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager:
    def __init__(self):
        self.current_cars = []
        self.move_distance = STARTING_MOVE_DISTANCE
        self.last_generation = -600

    class Car(Turtle):
        def __init__(self):
            super().__init__()
            self.shape("square")
            self.color(random.choice(COLORS))
            self.shapesize(stretch_wid=1, stretch_len=2)
            self.penup()
            self.speed(0)
            self.goto(320, random.randint(-200, 260))

    def generate_car(self):
        car = self.Car()
        if abs(car.ycor() - self.last_generation) <= 40:
            car.hideturtle()
            car.clear()
        else:
            self.current_cars.append(car)
            self.last_generation = car.ycor()

    def delete_hidden_cars(self):
        for car in self.current_cars:
            if car.xcor() < -320:
                self.current_cars.remove(car)
                car.clear()
                car.hideturtle()

    def move_cars(self):
        for car in self.current_cars:
            car.goto(car.xcor() - self.move_distance, car.ycor())

    def increase_speed(self):
        self.move_distance += MOVE_INCREMENT
