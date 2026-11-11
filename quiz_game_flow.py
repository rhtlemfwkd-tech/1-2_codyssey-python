"""퀴즈 진행·등록·목록·최고 점수를 관리하는 게임 흐름을 정의한다."""

from multiple_choice_question import MultipleChoiceQuestion
import quiz_json_save_load


class QuizGame:
    def __init__(self):
        # 저장 파일이 모두 손상된 경우에는 원본 보호를 위해 저장을 차단한다.
        self.questions, self.best_result, self.can_save = quiz_json_save_load.load_quiz_state()

    def save_progress(self):
        if not self.can_save:
            print("데이터 보호: 손상된 저장 파일이 있어 자동 저장을 차단했습니다.")
            return False
        return quiz_json_save_load.save_quiz_state(self.questions, self.best_result)

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

    @staticmethod
    def _ask_text(message):
        while True:
            value = input(message).strip()
            if value:
                return value
            print("빈 입력은 허용되지 않습니다.")

    @staticmethod
    def _ask_answer(message):
        while True:
            value = input(message).strip()
            if not value:
                print("빈 입력입니다.")
                continue
            try:
                answer = int(value)
            except ValueError:
                print("숫자를 입력해주세요.")
                continue
            if 1 <= answer <= 4:
                return answer
            print("1~4 사이의 숫자를 입력해주세요.")

    def play_quiz(self):
        if not self.questions:
            print("등록된 퀴즈가 없습니다.")
            return

        correct_count = 0
        total = len(self.questions)
        print(f"\n퀴즈를 시작합니다! 총 {total}문제")

        for number, quiz in enumerate(self.questions, start=1):
            print(f"\n[문제 {number}]")
            quiz.show_question()
            try:
                answer = self._ask_answer("정답 입력 (1~4): ")
            except (KeyboardInterrupt, EOFError):
                print("\n퀴즈를 중단하고 메뉴로 돌아갑니다.")
                return

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

        if self.best_result is None or score > self.best_result["score"]:
            self.best_result = {
                "score": score,
                "correct": correct_count,
                "total": total,
            }
            print("새로운 최고 점수입니다!")
            self.save_progress()

    def add_question(self):
        print("\n새로운 퀴즈를 추가합니다.")
        try:
            question = self._ask_text("문제: ")
            choices = [
                self._ask_text(f"선택지 {number}: ")
                for number in range(1, 5)
            ]
            answer = self._ask_answer("정답 번호 (1~4): ")
        except (KeyboardInterrupt, EOFError):
            print("\n퀴즈 등록을 취소했습니다.")
            return

        self.questions.append(MultipleChoiceQuestion(question, choices, answer))
        print("퀴즈가 추가되었습니다!")
        self.save_progress()

    def show_question_list(self):
        print("\n========================================")
        print("          등록된 퀴즈 목록")
        print("========================================")
        if not self.questions:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"총 {len(self.questions)}개의 퀴즈가 있습니다.\n")
        for number, quiz in enumerate(self.questions, start=1):
            print(f"[{number}] {quiz.question}")
        print("========================================")

    def show_best_score(self):
        if self.best_result is None:
            print("\n아직 퀴즈를 풀지 않았습니다.")
            return
        print("\n========================================")
        print("              최고 점수")
        print("========================================")
        print(f"최고 점수: {self.best_result['score']}점")
        print(
            f"정답: {self.best_result['total']}문제 중 "
            f"{self.best_result['correct']}문제"
        )
        print("========================================")

    def run_menu(self):
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
                self.play_quiz()
            elif choice == 2:
                self.add_question()
            elif choice == 3:
                self.show_question_list()
            elif choice == 4:
                self.show_best_score()
            elif choice == 5:
                print("게임을 종료합니다.")
                break
            else:
                print("1~5 사이의 숫자를 입력해주세요.")
