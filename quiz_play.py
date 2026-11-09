def play_quiz(quizzes):
    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
        return None

    correct_count = 0
    total = len(quizzes)

    print(f"\n퀴즈를 시작합니다! 총 {total}문제")

    for number, quiz in enumerate(quizzes, start=1):
        print(f"\n[문제 {number}]")
        quiz.show_question()

        while True:
            try:
                value = input("정답 입력 (1~4): ").strip()

                if not value:
                    print("빈 입력입니다.")
                    continue

                answer = int(value)

                if answer not in (1, 2, 3, 4):
                    print("1~4 사이의 숫자를 입력하세요.")
                    continue

                break

            except ValueError:
                print("숫자를 입력해주세요.")

            except (KeyboardInterrupt, EOFError):
                print("\n퀴즈를 중단하고 메뉴로 돌아갑니다.")
                return None

        if quiz.check_answer(answer):
            print("정답입니다!")
            correct_count += 1
        else:
            print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

    score = round(correct_count / total * 100)

    print("\n========================================")
    print(f"결과: {total}문제 중 {correct_count}문제 정답")
    print(f"점수: {score}점")
    print("========================================")

    return correct_count, total
