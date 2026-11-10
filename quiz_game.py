import json
import os
import tempfile
from pathlib import Path

from quiz import Quiz
from default_quizzes import create_default_quizzes
from quiz_play import play_quiz
from quiz_add import add_quiz
from quiz_list import show_quiz_list
from score import update_best_score, show_best_score


STATE_PATH = Path(__file__).resolve().parent / "state.json"
BACKUP_PATH = STATE_PATH.with_name("state.json.bak")


class QuizGame:
    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.best_result = None
        self.load_state()

    def save_state(self):
        data = {
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer
                }
                for quiz in self.quizzes
            ],
            "best_score": self.best_result
        }

        try:
            for target in (STATE_PATH, BACKUP_PATH):
                temporary = None
                try:
                    with tempfile.NamedTemporaryFile(
                        mode="w",
                        encoding="utf-8",
                        dir=STATE_PATH.parent,
                        prefix=f".{target.name}.",
                        suffix=".tmp",
                        delete=False,
                    ) as file:
                        temporary = file.name
                        json.dump(data, file, ensure_ascii=False, indent=2)
                        file.flush()
                        os.fsync(file.fileno())

                    os.replace(temporary, target)
                finally:
                    if temporary and os.path.exists(temporary):
                        os.unlink(temporary)

            print("데이터를 저장했습니다.")
            return True

        except OSError as error:
            print(f"데이터 저장 실패: {error}")
            return False

    def load_state(self, path=STATE_PATH):
        if not path.exists():
            if path == STATE_PATH and BACKUP_PATH.exists():
                print("원본 파일이 없어 백업을 확인합니다.")
                return self.load_state(BACKUP_PATH)

            print("저장 파일이 없어 기본 퀴즈를 사용합니다.")
            return

        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("데이터 형식이 올바르지 않습니다.")

            if not isinstance(data.get("quizzes"), list):
                raise ValueError("퀴즈 목록 형식이 잘못되었습니다.")

            loaded_quizzes = []

            for item in data["quizzes"]:
                if not isinstance(item, dict):
                    raise ValueError("퀴즈 데이터가 잘못되었습니다.")

                question = item["question"]
                choices = item["choices"]
                answer = item["answer"]

                if (
                    not isinstance(question, str)
                    or not question.strip()
                    or not isinstance(choices, list)
                    or len(choices) != 4
                    or not all(
                        isinstance(choice, str) and choice.strip()
                        for choice in choices
                    )
                    or type(answer) is not int
                ):
                    raise ValueError("퀴즈 데이터가 유효하지 않습니다.")

                loaded_quizzes.append(
                    Quiz(question, choices, answer)
                )

            best = data.get("best_score")

            if best is not None:
                if (
                    not isinstance(best, dict)
                    or not all(
                        type(best.get(key)) is int
                        for key in ("score", "correct", "total")
                    )
                    or best["total"] <= 0
                    or not 0 <= best["correct"] <= best["total"]
                    or best["score"] != round(
                        best["correct"] / best["total"] * 100
                    )
                ):
                    raise ValueError("최고 점수 데이터가 잘못되었습니다.")

            self.quizzes = loaded_quizzes
            self.best_result = best

            print(f"저장된 퀴즈 {len(self.quizzes)}개를 불러왔습니다.")

            if path == BACKUP_PATH:
                print("백업 파일에서 데이터를 복구했습니다.")
                self.save_state()

        except (OSError, UnicodeError, ValueError, TypeError, KeyError) as error:
            print(f"데이터 불러오기 실패 ({path.name}): {error}")

            if path == STATE_PATH and BACKUP_PATH.exists():
                print("백업 파일 복구를 시도합니다.")
                return self.load_state(BACKUP_PATH)

            print("사용 가능한 백업이 없어 기본 퀴즈와 초기 점수로 복구합니다.")
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
            self.save_state()

    def add(self):
        if add_quiz(self.quizzes):
            self.save_state()

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
