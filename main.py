from quiz_game import QuizGame


def main():
    game = QuizGame()

    try:
        game.run()
    finally:
        game.save_state()


if __name__ == "__main__":
    main()
