from datetime import datetime

def calculate_score(
    test_results: dict,
    submission_time: datetime,
    deadline: datetime,
    code_quality_score: float,
    plagiarism_score: float,
    weights: dict = None
) -> float:
    if weights is None:
        weights = {
            "test_results": 0.6,
            "submission_time": 0.2,
            "code_quality": 0.1,
            "plagiarism": 0.1
        }

    if test_results["total"] > 0:
        test_score = (test_results["passed"] / test_results["total"]) * 100
    else:
        test_score = 0

    time_diff = (deadline - submission_time).total_seconds()
    if time_diff > 0:
        max_bonus_time = 7 * 24 * 60 * 60  # 7 days in seconds
        submission_bonus = min(100, (time_diff / max_bonus_time) * 100)
    else:
        submission_bonus = 0

    plagiarism_penalty = max(0, 100 - plagiarism_score)

    final_score = (
        weights["test_results"] * test_score +
        weights["submission_time"] * submission_bonus +
        weights["code_quality"] * code_quality_score +
        weights["plagiarism"] * plagiarism_penalty
    )

    return min(100, final_score)