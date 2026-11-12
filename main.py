from quiz_game_flow import QuizGame


def main():
    game = QuizGame()

    try:
        game.run_menu()
    finally:
        game.save_progress()


if __name__ == "__main__":
    main()
