import json
from datetime import datetime
from pathlib import Path

from backend.core.database import get_connection


PROJECT_ROOT = Path(__file__).resolve().parents[2]
QUIZ_FILE = PROJECT_ROOT / "awareness" / "quiz.json"


def get_modules():
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                id,
                title,
                category,
                difficulty,
                content
            FROM awareness_modules
            ORDER BY id
            """
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


def get_quiz():
    if not QUIZ_FILE.exists():
        return []

    with open(
        QUIZ_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def submit_quiz(score, total):
    score = int(score)
    total = int(total)

    if total <= 0:
        raise ValueError(
            "Quiz total must be greater than zero."
        )

    if score < 0 or score > total:
        raise ValueError(
            "Quiz score is outside the valid range."
        )

    percentage = round(
        (score / total) * 100,
        2
    )

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO quiz_results (
                score,
                total,
                percentage,
                submitted_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                score,
                total,
                percentage,
                datetime.utcnow().isoformat()
            )
        )

        connection.commit()

    finally:
        connection.close()

    if percentage >= 80:
        recommendation = (
            "Strong security awareness. "
            "Continue practicing with advanced scenarios."
        )
    elif percentage >= 60:
        recommendation = (
            "Good foundation. "
            "Review the modules where you missed questions."
        )
    else:
        recommendation = (
            "Review the awareness modules and "
            "retake the quiz to reinforce the fundamentals."
        )

    return {
        "score": score,
        "total": total,
        "percentage": percentage,
        "recommendation": recommendation
    }