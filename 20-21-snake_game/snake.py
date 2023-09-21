import time
from turtle import Turtle, Screen

MOVE_DISTANCE = 20
UP = 90
RIGHT = 0
LEFT = 180
DOWN = 270
INITIAL_SNAKE = 3

class Snake:

    def __init__(self):
        # Snake setup
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        for segment_num in range(INITIAL_SNAKE):
            segment = Turtle(shape="square")
            segment.speed(1)
            segment.penup()
            segment.color("white")
            if segment_num == 0:
                segment.goto(0, 0)
            else:
                starting_pos = self.segments[segment_num - 1].xcor() - 20
                segment.goto(x=starting_pos, y=0)
            self.segments.append(segment)

    def extend(self):
        last_segment_pos = self.segments[-1].pos()
        segment = Turtle(shape="square")
        segment.speed(1)
        segment.penup()
        segment.color("white")
        segment.goto(last_segment_pos)
        self.segments.append(segment)

    def move(self):
        for i in range(len(self.segments) - 1, 0, -1):
            new_pos = self.segments[i - 1].pos()
            self.segments[i].goto(new_pos)
        self.segments[0].forward(MOVE_DISTANCE)

    def right(self):
        if self.head.heading() == LEFT:
            pass
        else:
            self.head.setheading(RIGHT)

    def left(self):
        if self.head.heading() == RIGHT:
            pass
        else:
            self.head.setheading(LEFT)

    def up(self):
        if self.head.heading() == DOWN:
            pass
        else:
            self.head.setheading(UP)

    def down(self):
        if self.head.heading() == UP:
            pass
        else:
            self.head.setheading(DOWN)

    def reset_snake(self):
        for segment in self.segments:
            segment.goto(1000, 1000)
        self.segments.clear()
        time.sleep(1)
        self.create_snake()
        self.head = self.segments[0]


