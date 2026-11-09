class Quiz:
    def __init__(self, question, choices, answer):
        if len(choices) != 4:
            raise ValueError("선택지는 4개여야 합니다.")

        if answer not in (1, 2, 3, 4):
            raise ValueError("정답은 1~4 사이여야 합니다.")

        self.question = question
        self.choices = choices
        self.answer = answer

    def show_question(self):
        print()
        print(self.question)

        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def check_answer(self, user_answer):
        return self.answer == user_answer
