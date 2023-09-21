class QuizzBrain:

    def __init__(self, questions_data):
        self.question_number = 0
        self.score = 0
        self.question_list = questions_data


    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        current_question = self.question_list[self.question_number]
        user_answer = input(f"Q.{self.question_number + 1}: {current_question.text} (True/False)?")
        self.check_answer(user_answer, current_question.answer)
        self.question_number += 1

    def check_answer(self, user_answer, correct_answer):
        if user_answer == correct_answer:
            print(f"You're right! The answer is {correct_answer}")
            self.score += 1
        else:
            print(f"Wrong... The correc answer was {correct_answer}")
            pass
        print(f"Score: {self.score}/{self.question_number + 1}")
