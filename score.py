def update_best_score(best_result, correct_count, total):
    if total <= 0:
        return best_result, False

    score = round(correct_count / total * 100)

    if best_result is None or score > best_result["score"]:
        best_result = {
            "score": score,
            "correct": correct_count,
            "total": total
        }
        return best_result, True

    return best_result, False


def show_best_score(best_result):
    if best_result is None:
        print("\n아직 퀴즈를 풀지 않았습니다.")
        return

    print("\n========================================")
    print("              최고 점수")
    print("========================================")
    print(f"최고 점수: {best_result['score']}점")
    print(
        f"정답: {best_result['total']}문제 중 "
        f"{best_result['correct']}문제"
    )
    print("========================================")
