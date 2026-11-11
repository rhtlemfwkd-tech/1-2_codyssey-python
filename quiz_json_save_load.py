"""퀴즈 목록과 최고 점수를 JSON 파일에 저장·읽기·검증·백업 복구한다."""

import json
import os
import tempfile
from pathlib import Path

from multiple_choice_question import MultipleChoiceQuestion
from default_quiz_questions import create_default_questions

STATE_PATH = Path(__file__).resolve().parent / "state.json"
BACKUP_PATH = STATE_PATH.with_name("state.json.bak")


def _read_file(path):
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict) or not isinstance(data.get("quizzes"), list):
        raise ValueError("퀴즈 목록 형식이 잘못되었습니다.")

    quizzes = []
    for item in data["quizzes"]:
        if not isinstance(item, dict):
            raise ValueError("퀴즈 데이터가 잘못되었습니다.")
        question, choices, answer = (
            item["question"], item["choices"], item["answer"]
        )
        if (
            not isinstance(question, str) or not question.strip()
            or not isinstance(choices, list) or len(choices) != 4
            or not all(isinstance(c, str) and c.strip() for c in choices)
            or type(answer) is not int
        ):
            raise ValueError("퀴즈 데이터가 유효하지 않습니다.")
        quizzes.append(MultipleChoiceQuestion(question, choices, answer))

    best = data.get("best_score")
    if best is not None and (
        not isinstance(best, dict)
        or not all(type(best.get(k)) is int for k in ("score", "correct", "total"))
        or best["total"] <= 0
        or not 0 <= best["correct"] <= best["total"]
        or best["score"] != round(best["correct"] / best["total"] * 100)
    ):
        raise ValueError("최고 점수 데이터가 잘못되었습니다.")

    return quizzes, best


def _write_atomic(path, data):
    """같은 디렉터리에 임시 파일을 쓴 뒤 단일 파일을 교체한다."""
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as file:
            temp_name = file.name
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temp_name, path)
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)


def save_quiz_state(questions, best_result):
    data = {
        "quizzes": [
            {"question": q.question, "choices": q.choices, "answer": q.answer}
            for q in questions
        ],
        "best_score": best_result,
    }
    try:
        # 원본과 백업은 각각 교체하며 두 파일의 갱신은 트랜잭션이 아니다.
        for target in (STATE_PATH, BACKUP_PATH):
            _write_atomic(target, data)
        print("데이터를 저장했습니다.")
        return True
    except OSError as error:
        print(f"데이터 저장 실패: {error}")
        return False


def load_quiz_state():
    """(퀴즈, 최고 기록, 저장 가능 여부)를 반환한다."""
    found = False
    for path in (STATE_PATH, BACKUP_PATH):
        if not path.exists():
            continue
        found = True
        try:
            quizzes, best = _read_file(path)
        except (OSError, UnicodeError, ValueError, TypeError, KeyError) as error:
            print(f"데이터 불러오기 실패 ({path.name}): {error}")
            continue

        print(f"저장된 퀴즈 {len(quizzes)}개를 불러왔습니다.")
        if path == BACKUP_PATH:
            print("백업 파일에서 데이터를 복구했습니다.")
            save_quiz_state(quizzes, best)
        return quizzes, best, True

    if not found:
        print("저장 파일이 없어 기본 퀴즈를 사용합니다.")
        return create_default_questions(), None, True

    # 둘 다 손상되었거나 읽을 수 없는 경우 덮어쓰지 않는다.
    print("사용 가능한 백업이 없어 기본 퀴즈를 메모리에서 사용합니다.")
    print("손상된 원본을 보존하기 위해 이번 실행의 자동 저장을 차단합니다.")
    return create_default_questions(), None, False
