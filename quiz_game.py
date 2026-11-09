from default_quizzes import create_default_quizzes
from quiz_play import play_quiz
from quiz_add import add_quiz
from quiz_list import show_quiz_list
from score import update_best_score, show_best_score


class QuizGame:
    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.best_result = None

    def show_menu(self):
        print("\n========================================")
        print("         Python 기초 퀴즈 게임")
        print("========================================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("========================================")

    def play(self):
        result = play_quiz(self.quizzes)

        if result is None:
            return

        correct_count, total = result

        self.best_result, is_new_record = update_best_score(
            self.best_result, correct_count, total
        )

        if is_new_record:
            print("새로운 최고 점수입니다!")

    def add(self):
        add_quiz(self.quizzes)

    def show_list(self):
        show_quiz_list(self.quizzes)

    def show_score(self):
        show_best_score(self.best_result)

    def run(self):
        while True:
            self.show_menu()

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
                self.play()
            elif choice == 2:
                self.add()
            elif choice == 3:
                self.show_list()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                print("게임을 종료합니다.")
                break
            else:
                print("1~5 사이의 숫자를 입력해주세요.")
