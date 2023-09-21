import time
from turtle import Screen
from player import Player, FINISH_LINE_Y
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)
screen.listen()

player = Player()
print(player.shapesize())
scoreboard = Scoreboard()
car_manager = CarManager()

screen.onkeypress(player.move_up, "Up")
screen.onkeypress(player.move_down, "Down")


game_is_on = True
iteration_count = 0
interval = 5
while game_is_on:
    time.sleep(0.1)
    screen.update()
    iteration_count += 1

    if iteration_count >= interval:
        car_manager.generate_car()
        iteration_count = 0
    car_manager.move_cars()
    car_manager.delete_hidden_cars()

    if player.ycor() > FINISH_LINE_Y:
        player.reset_position()
        scoreboard.increase_score()
        car_manager.increase_speed()
        interval -= 2

    for car in car_manager.current_cars:
        if abs(player.ycor()-car.ycor()) < 17 and abs(player.xcor()- car.xcor()) < 33:
            game_is_on = False

scoreboard.game_over()

screen.exitonclick()



