from quiz_list import show_quiz_list
from quiz_add import add_quiz
from default_quizzes import create_default_quizzes
from quiz_play import play_quiz
def show_menu():
    print("\n========================================")
    print("         Python 기초 퀴즈 게임")
    print("========================================")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("========================================")


def main():
    quizzes = create_default_quizzes()

    while True:
        show_menu()

        try:
            value = input("선택: ").strip()

            if not value:
                print("빈 입력입니다.")
                continue

            choice = int(value)

        except ValueError:
            print("숫자를 입력해주세요.")
            continue

        except (KeyboardInterrupt, EOFError):
            print("\n안전하게 종료합니다.")
            break

        if choice == 1:
            play_quiz(quizzes)
        elif choice == 2:
            add_quiz(quizzes)
        elif choice == 3:
            show_quiz_list(quizzes)
        elif choice == 4:
            print("점수 확인 (준비 중)")
        elif choice == 5:
            print("게임을 종료합니다.")
            break
        else:
            print("1~5 사이의 숫자를 입력해주세요.")


if __name__ == "__main__":
    main()
