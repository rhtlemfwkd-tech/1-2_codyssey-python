# Python Quiz Game

Python 기초 문법과 객체 지향 프로그래밍을 학습하기 위해
제작한 터미널 기반 퀴즈 게임입니다.

## 1. 프로젝트 개요

사용자가 퀴즈를 풀거나 새로운 문제를 등록할 수 있는
Python 콘솔 프로그램입니다.

Quiz와 QuizGame 클래스를 통해 역할을 분리하고,
JSON 파일을 이용해 퀴즈와 최고 점수를 영구 저장합니다.

## 2. 퀴즈 주제 및 선정 이유

주제: Linux, Docker, Git, Python 기초

개발 교육 과정에서 학습한 내용을 복습하고,
실제 개발 환경에서 사용하는 기본 개념을
확실하게 이해하기 위해 선정했습니다.

## 3. 개발 환경

- Python 3.10 이상 (개발 환경: Python 3.13.17)
- Git
- Windows / Git Bash
- Python 표준 라이브러리 사용
- 외부 패키지 설치 불필요

## 4. 실행 방법

저장소를 복제한 뒤 프로젝트 폴더에서 실행합니다.

    git clone https://github.com/rhtlemfwkd-tech/1-2_codyssey-python.git
    cd 1-2_codyssey-python
    python main.py

Python 실행 명령은 운영체제 환경에 따라 다를 수 있습니다.

## 5. 주요 기능

1. 퀴즈 풀기
   - 등록된 문제 출제
   - 정답 및 오답 판정
   - 정답률 기반 점수 계산

2. 퀴즈 추가
   - 문제와 선택지 4개 입력
   - 정답 번호 지정
   - JSON 파일에 저장

3. 퀴즈 목록
   - 등록된 모든 문제 확인
   - 문제 개수 표시

4. 점수 확인
   - 최고 점수 확인
   - 기존 기록보다 높으면 갱신
   - 프로그램 재실행 후에도 기록 유지

5. 종료
   - 안전한 프로그램 종료
   - 종료 시 데이터 저장

## 6. 프로젝트 파일 구조

    1-2_codyssey-python/
    ├── main.py
    ├── quiz.py
    ├── quiz_game.py
    ├── quiz_play.py
    ├── quiz_add.py
    ├── quiz_list.py
    ├── score.py
    ├── default_quizzes.py
    ├── state.json
    ├── .gitignore
    ├── README.md
    └── docs/
        └── screenshots/

state.json은 실행 시 생성되는 로컬 데이터 파일입니다.

## 7. 클래스 구조

### Quiz

개별 퀴즈를 표현하는 클래스입니다.

- question: 문제 내용
- choices: 선택지 4개
- answer: 정답 번호
- show_question(): 문제 출력
- check_answer(): 정답 확인

### QuizGame

게임 전체의 실행과 상태를 관리하는 클래스입니다.

- quizzes: 퀴즈 목록
- best_result: 최고 점수 기록
- run(): 메뉴 실행
- play(): 퀴즈 진행
- add(): 퀴즈 등록
- show_list(): 목록 출력
- show_score(): 최고 점수 확인
- save_state(): JSON 저장
- load_state(): JSON 불러오기

## 8. 데이터 파일 (state.json)

프로젝트 루트의 state.json에 UTF-8 형식으로 저장합니다.

데이터의 주요 필드는 다음과 같습니다.

- quizzes: 퀴즈 객체의 데이터 목록
- question: 문제 문자열
- choices: 선택지 문자열 목록
- answer: 정답 번호 (1~4)
- best_score: 최고 점수 기록
- score: 100점 기준 점수
- correct: 정답 개수
- total: 전체 문제 수

best_score는 기록이 없을 때 null이며,
기록이 있으면 score, correct, total을 가진 객체입니다.

파일이 없으면 기본 퀴즈 5개로 시작합니다.
파일이 손상되면 안내 메시지를 출력하고 초기화합니다.

state.json은 .gitignore에 등록되어 Git에 포함되지 않습니다.

## 9. 예외 처리

- 숫자가 아닌 입력 처리
- 빈 입력 및 앞뒤 공백 처리
- 메뉴와 정답 번호의 범위 검사
- Ctrl+C 및 EOF 입력 처리
- JSON 파일 누락 및 손상 복구
- 파일 입출력 오류 처리

## 10. Git 학습 내용

- git init / add / commit / push
- git checkout을 이용한 브랜치 생성 및 전환
- git merge를 이용한 기능 브랜치 병합
- git clone을 이용한 저장소 복제
- git pull을 이용한 원격 변경사항 동기화

기능별 커밋으로 개발 이력을 관리했습니다.

## 11. 학습 내용

- 변수와 기본 자료형
- 조건문과 반복문
- 함수와 반환값
- 클래스와 객체
- 리스트와 딕셔너리
- JSON 파일 입출력
- 예외 처리
- Git 버전 관리
