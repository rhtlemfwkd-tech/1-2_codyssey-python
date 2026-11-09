from quiz import Quiz


def ask_text(message):
    while True:
        value = input(message).strip()

        if value:
            return value

        print("빈 입력은 허용되지 않습니다.")


def ask_answer():
    while True:
        value = input("정답 번호 (1~4): ").strip()

        try:
            answer = int(value)
        except ValueError:
            print("숫자를 입력해주세요.")
            continue

        if 1 <= answer <= 4:
            return answer

        print("1~4 사이의 숫자를 입력해주세요.")


def add_quiz(quizzes):
    print("\n새로운 퀴즈를 추가합니다.")

    try:
        question = ask_text("문제: ")

        choices = []

        for number in range(1, 5):
            choice = ask_text(f"선택지 {number}: ")
            choices.append(choice)

        answer = ask_answer()

    except (KeyboardInterrupt, EOFError):
        print("\n퀴즈 등록을 취소했습니다.")
        return False

    new_quiz = Quiz(question, choices, answer)
    quizzes.append(new_quiz)

    print("퀴즈가 추가되었습니다!")
    return True
