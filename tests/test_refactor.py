"""표준 라이브러리만 사용한 회귀 테스트: python -m unittest discover -s tests -v"""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import quiz_json_save_load
from multiple_choice_question import MultipleChoiceQuestion
from quiz_game_flow import QuizGame


class QuizRefactorTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        self.state = root / "state.json"
        self.backup = root / "state.json.bak"
        self.original_state = quiz_json_save_load.STATE_PATH
        self.original_backup = quiz_json_save_load.BACKUP_PATH
        quiz_json_save_load.STATE_PATH = self.state
        quiz_json_save_load.BACKUP_PATH = self.backup
        self.output = io.StringIO()
        self.capture = contextlib.redirect_stdout(self.output)
        self.capture.__enter__()

    def tearDown(self):
        self.capture.__exit__(None, None, None)
        quiz_json_save_load.STATE_PATH = self.original_state
        quiz_json_save_load.BACKUP_PATH = self.original_backup
        self.temp_dir.cleanup()

    def test_default_questions_and_quit(self):
        game = QuizGame()
        self.assertEqual(len(game.questions), 5)
        with patch("builtins.input", return_value="5"):
            game.run_menu()
        self.assertIn("게임을 종료합니다.", self.output.getvalue())

    def test_add_play_list_score_and_reload(self):
        game = QuizGame()
        inputs = ["추가 문제?", "가", "나", "다", "라", "1"]
        with patch("builtins.input", side_effect=inputs):
            game.add_question()
        self.assertEqual(len(game.questions), 6)
        game.show_question_list()
        self.assertIn("추가 문제?", self.output.getvalue())
        with patch("builtins.input", side_effect=["2", "3", "4", "2", "1", "1"]):
            game.play_quiz()
        self.assertEqual(game.best_result, {"score": 100, "correct": 6, "total": 6})
        game.show_best_score()
        self.assertIn("최고 점수: 100점", self.output.getvalue())
        self.assertTrue(self.state.exists())
        self.assertTrue(self.backup.exists())
        reloaded = QuizGame()
        self.assertEqual(len(reloaded.questions), 6)
        self.assertEqual(reloaded.best_result["score"], 100)

    def test_add_interrupt_does_not_create_quiz(self):
        game = QuizGame()
        with patch("builtins.input", side_effect=["문제?", "가", "나", KeyboardInterrupt]):
            game.add_question()
        self.assertEqual(len(game.questions), 5)
        self.assertFalse(self.state.exists())
        self.assertIn("퀴즈 등록을 취소했습니다.", self.output.getvalue())

    def test_invalid_answer_retries(self):
        game = QuizGame()
        with patch("builtins.input", side_effect=["", "문자", "9", "2", "3", "4", "2", "1"]):
            game.play_quiz()
        self.assertEqual(game.best_result["score"], 100)
        log = self.output.getvalue()
        self.assertIn("빈 입력입니다.", log)
        self.assertIn("숫자를 입력해주세요.", log)
        self.assertIn("1~4 사이의 숫자를 입력해주세요.", log)

    def test_legacy_json_compatibility(self):
        data = {
            "quizzes": [{"question": "이전 문제", "choices": ["1", "2", "3", "4"], "answer": 3}],
            "best_score": {"score": 50, "correct": 1, "total": 2},
        }
        self.state.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        game = QuizGame()
        self.assertEqual(len(game.questions), 1)
        self.assertEqual(game.best_result["score"], 50)
        self.assertTrue(game.save_progress())
        self.assertEqual(json.loads(self.state.read_text(encoding="utf-8")), data)

    def test_corrupted_original_restores_backup(self):
        game = QuizGame()
        game.questions.append(MultipleChoiceQuestion("백업 검증?", ["a", "b", "c", "d"], 2))
        game.best_result = {"score": 80, "correct": 4, "total": 5}
        self.assertTrue(game.save_progress())
        self.state.write_text("{ invalid json", encoding="utf-8")
        restored = QuizGame()
        self.assertTrue(restored.can_save)
        self.assertEqual(len(restored.questions), 6)
        self.assertEqual(restored.best_result["score"], 80)
        self.assertEqual(len(json.loads(self.state.read_text(encoding="utf-8"))["quizzes"]), 6)

    def test_missing_original_restores_backup(self):
        game = QuizGame()
        self.assertTrue(game.save_progress())
        self.state.unlink()
        restored = QuizGame()
        self.assertEqual(len(restored.questions), 5)
        self.assertTrue(self.state.exists())

    def test_both_corrupt_preserved_without_overwrite(self):
        self.state.write_text("broken original", encoding="utf-8")
        self.backup.write_text("broken backup", encoding="utf-8")
        game = QuizGame()
        self.assertFalse(game.can_save)
        self.assertEqual(len(game.questions), 5)
        self.assertFalse(game.save_progress())
        self.assertEqual(self.state.read_text(encoding="utf-8"), "broken original")
        self.assertEqual(self.backup.read_text(encoding="utf-8"), "broken backup")

    def test_empty_quiz_set(self):
        game = QuizGame()
        game.questions.clear()
        game.play_quiz()
        game.show_question_list()
        self.assertIn("등록된 퀴즈가 없습니다.", self.output.getvalue())

    def test_menu_eof(self):
        game = QuizGame()
        with patch("builtins.input", side_effect=EOFError):
            game.run_menu()
        self.assertIn("안전하게 종료합니다.", self.output.getvalue())


if __name__ == "__main__":
    unittest.main()
