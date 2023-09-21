from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz_brain = quiz_brain

        self.window = Tk()
        self.window.title("Quizz App")
        self.window.config(bg=THEME_COLOR, padx=20, pady=20)
        self.canvas = Canvas(self.window, height=250, width=300, bg="white")
        self.canvas.grid(column=0, columnspan=2, row=1, pady=20, )
        self.question_text = self.canvas.create_text(
            150,
            125,
            text="Test",
            fill=THEME_COLOR,
            font=("Ariel", 15, "italic"),
            width=300
        )

        true_background = PhotoImage(file="./images/true.png")
        false_background = PhotoImage(file="./images/false.png")
        self.true_button = Button(image=true_background, command=self.true_pressed)
        self.false_button = Button(image=false_background, command=self.false_pressed)
        self.true_button.grid(column=0, row=2)
        self.false_button.grid(column=1, row=2)

        self.score_label = Label(
            text=f"Score: {self.quiz_brain.score}",
            fg="white", bg=THEME_COLOR,
            font=("Ariel", 15, "italic")
        )

        self.score_label.grid(column=1, row=0)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        if self.quiz_brain.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz_brain.score}")
            self.canvas.config(bg="white")
            q_text = self.quiz_brain.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.score_label.config(text=f"Score: {self.quiz_brain.score}")
            self.finish_game()

    def true_pressed(self):
        is_correct = self.quiz_brain.check_answer("True")
        self.give_feedback(is_correct)

    def false_pressed(self):
        is_correct = self.quiz_brain.check_answer("False")
        self.give_feedback(is_correct)

    def give_feedback(self, is_correct):
        if is_correct:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000, self.get_next_question)

    def finish_game(self):
        self.canvas.config(bg="White")
        self.canvas.itemconfig(self.question_text, text=f"The end\nScore: {self.quiz_brain.score}/10")
        self.true_button.config(state="disabled")
        self.false_button.config(state="disabled")
        self.window.after(5000, self.window.destroy)
