"""프로그램을 처음 실행할 때 사용할 기본 객관식 문제 5개를 생성한다."""

from multiple_choice_question import MultipleChoiceQuestion


def create_default_questions():
    return [
        MultipleChoiceQuestion(
            "현재 작업 디렉터리를 출력하는 Linux 명령어는?",
            ["cd", "pwd", "ls", "mkdir"],
            2
        ),
        MultipleChoiceQuestion(
            "Docker 이미지와 컨테이너의 관계로 올바른 것은?",
            [
                "이미지는 실행 중인 프로세스다",
                "컨테이너는 이미지를 삭제하는 명령어다",
                "컨테이너는 이미지를 기반으로 생성된다",
                "이미지와 컨테이너는 완전히 동일하다"
            ],
            3
        ),
        MultipleChoiceQuestion(
            "Git에서 변경사항을 커밋하는 명령어는?",
            ["git push", "git clone", "git pull", "git commit"],
            4
        ),
        MultipleChoiceQuestion(
            "Python에서 리스트를 나타내는 기호는?",
            ["{}", "[]", "()", "<>"],
            2
        ),
        MultipleChoiceQuestion(
            "Python의 dict 자료형은 무엇을 저장할까?",
            [
                "키와 값의 쌍",
                "정수만",
                "문자 하나만",
                "참 또는 거짓만"
            ],
            1
        )
    ]
