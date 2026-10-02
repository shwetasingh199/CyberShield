import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.database import (
    get_connection,
    initialize_database
)


MODULES = [
    {
        "title": "Phishing Awareness",
        "category": "PHISHING",
        "difficulty": "BEGINNER",
        "content": (
            "Learn how to recognize suspicious emails, "
            "unexpected links, impersonation attempts and "
            "credential harvesting indicators."
        )
    },
    {
        "title": "Password & Authentication Security",
        "category": "ACCOUNT SECURITY",
        "difficulty": "BEGINNER",
        "content": (
            "Learn secure password practices, multi-factor "
            "authentication and account protection techniques."
        )
    },
    {
        "title": "Safe Web Browsing",
        "category": "WEB SECURITY",
        "difficulty": "INTERMEDIATE",
        "content": (
            "Understand suspicious websites, unsafe downloads, "
            "browser warnings and secure browsing practices."
        )
    },
    {
        "title": "Social Engineering Defense",
        "category": "SOCIAL ENGINEERING",
        "difficulty": "INTERMEDIATE",
        "content": (
            "Learn how attackers use urgency, authority, trust "
            "and manipulation to influence users."
        )
    },
    {
        "title": "Incident Reporting",
        "category": "INCIDENT RESPONSE",
        "difficulty": "INTERMEDIATE",
        "content": (
            "Learn what information should be reported when a "
            "security incident or suspicious activity is discovered."
        )
    }
]


def seed_awareness():
    initialize_database()

    connection = get_connection()

    try:
        existing = connection.execute(
            "SELECT COUNT(*) FROM awareness_modules"
        ).fetchone()[0]

        if existing > 0:
            print(
                f"Awareness database already contains "
                f"{existing} modules."
            )
            print("No new modules were inserted.")
            return

        for module in MODULES:
            connection.execute(
                """
                INSERT INTO awareness_modules (
                    title,
                    category,
                    difficulty,
                    content
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    module["title"],
                    module["category"],
                    module["difficulty"],
                    module["content"]
                )
            )

        connection.commit()

        print()
        print("====================================")
        print("Awareness Seed Complete")
        print("====================================")
        print(
            f"Modules created: {len(MODULES)}"
        )

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    seed_awareness()