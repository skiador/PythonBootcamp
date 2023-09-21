from data import question_data
from quiz_brain import QuizzBrain


class Question:

    def __init__(self, q_text, q_answer):
        self.text = q_text
        self.answer = q_answer


question_bank = []
for question in question_data:
    question = Question(question["question"], question["correct_answer"])
    question_bank.append(question)


quiz = QuizzBrain(question_bank)
while quiz.still_has_questions():
    quiz.next_question()

print("Well done, you've completed the quizz!")
print(f"Your final score is {quiz.score}/{len(quiz.question_list)}.")
