from turtle import Turtle

FONT = ("Courier", 80, "normal")
END_GAME_FONT = ("Courier", 80, "normal")


class ScoreBoard(Turtle):

    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.r_score = 0
        self.l_score = 0
        self.speed(0)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(-100, 200)
        self.pendown()
        self.write(f"{self.r_score}", align="center", font=FONT)
        self.penup()
        self.goto(100, 200)
        self.pendown()
        self.write(f"{self.l_score}", align="center", font=FONT)
        self.penup()

    def end_game_score(self):
        self.clear()
        self.goto(0, 0)
        if self.r_score > self.l_score:
            self.write("Player 1 Wins!", align="center", font=END_GAME_FONT)
        else:
            self.write("PLayer 2 Wins!", align="center", font=END_GAME_FONT)

    def l_point(self):
        self.l_score += 1
        self.update_scoreboard()

    def r_point(self):
        self.r_score += 1
        self.update_scoreboard()



