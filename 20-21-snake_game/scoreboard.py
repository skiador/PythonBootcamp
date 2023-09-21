from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier", 20, "normal")


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.score = -1
        with open("high_score.txt") as file:
            self.high_score = int(file.read())
        self.goto(x=0, y=270)
        self.color("white")
        self.hideturtle()
        self.speed(0)
        self.increase_score()

    def update_score(self):
        self.clear()
        self.write(f"High Score: {self.high_score}  Score: {self.score}", align=ALIGNMENT, font=FONT)

    # def game_over(self):
    #     self.goto(0, 0)
    #     self.write(f"Game Over", align=ALIGNMENT, font=FONT)

    def reset_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("high_score.txt", mode="w") as file:
                file.write(f"{self.high_score}")
        self.score = 0
        self.update_score()

    def increase_score(self):
        self.score += 1
