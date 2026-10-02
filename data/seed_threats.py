import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from backend.core.database import get_connection, initialize_database
from backend.services.threat_service import create_threat
from backend.services.alert_service import create_alert_if_required


THREATS = [
    {
        "name": "Suspicious Credential Phishing Campaign",
        "category": "PHISHING",
        "description": "A simulated phishing campaign targeting user credentials through a suspicious web domain.",
        "severity": "CRITICAL",
        "confidence": 95,
        "indicator_value": "secure-login-example.com",
        "source": "Internal Threat Intelligence",
        "recency": 90,
        "frequency": 80,
        "source_reliability": "A",
        "correlation": 90
    },
    {
        "name": "Malware Delivery Infrastructure",
        "category": "MALWARE",
        "description": "A simulated indicator associated with malware delivery infrastructure.",
        "severity": "HIGH",
        "confidence": 88,
        "indicator_value": "203.0.113.45",
        "source": "Internal Threat Intelligence",
        "recency": 85,
        "frequency": 70,
        "source_reliability": "B",
        "correlation": 75
    },
    {
        "name": "Suspicious File Hash",
        "category": "MALWARE",
        "description": "A simulated SHA-256 file indicator requiring analyst review.",
        "severity": "HIGH",
        "confidence": 80,
        "indicator_value": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "source": "Endpoint Security",
        "recency": 70,
        "frequency": 65,
        "source_reliability": "B",
        "correlation": 60
    },
    {
        "name": "Exposed Web Application",
        "category": "WEB_THREAT",
        "description": "A simulated web application exposure associated with increased security risk.",
        "severity": "MEDIUM",
        "confidence": 75,
        "indicator_value": "portal-example.com",
        "source": "Security Assessment",
        "recency": 60,
        "frequency": 50,
        "source_reliability": "C",
        "correlation": 55
    },
    {
        "name": "Low Confidence Suspicious Email",
        "category": "SOCIAL_ENGINEERING",
        "description": "A simulated suspicious email indicator requiring monitoring.",
        "severity": "LOW",
        "confidence": 50,
        "indicator_value": "analyst@example.com",
        "source": "Email Security",
        "recency": 50,
        "frequency": 30,
        "source_reliability": "D",
        "correlation": 20
    }
]


def seed_threats():
    initialize_database()

    connection = get_connection()

    try:
        existing = connection.execute(
            "SELECT COUNT(*) FROM threats"
        ).fetchone()[0]

        if existing > 0:
            print(f"Threat database already contains {existing} records.")
            print("No new threat records were inserted.")
            return

    finally:
        connection.close()

    created = 0
    alerts = 0

    for threat in THREATS:
        try:
            threat_id = create_threat(threat)

            connection = get_connection()

            row = connection.execute(
                """
                SELECT
                    name,
                    severity,
                    risk_score,
                    description
                FROM threats
                WHERE id = ?
                """,
                (threat_id,)
            ).fetchone()

            connection.close()

            alert_id = create_alert_if_required(
                threat_id=threat_id,
                threat_name=row["name"],
                severity=row["severity"],
                risk_score=row["risk_score"],
                description=row["description"]
            )

            created += 1

            if alert_id:
                alerts += 1

            print(
                f"Created threat #{threat_id}: "
                f"{row['name']} "
                f"(risk={row['risk_score']})"
            )

        except Exception as error:
            print(
                f"Failed to create {threat['name']}: {error}"
            )

    print()
    print("====================================")
    print("CyberShield Threat Seed Complete")
    print("====================================")
    print(f"Threats created : {created}")
    print(f"Alerts created  : {alerts}")


if __name__ == "__main__":
    seed_threats()