def show_quiz_list(quizzes):
    print("\n========================================")
    print("          등록된 퀴즈 목록")
    print("========================================")

    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
        return

    print(f"총 {len(quizzes)}개의 퀴즈가 있습니다.\n")

    for number, quiz in enumerate(quizzes, start=1):
        print(f"[{number}] {quiz.question}")

    print("========================================")
