from datetime import datetime

from backend.core.database import get_connection
from backend.services.indicator_service import validate_indicator
from backend.services.risk_service import calculate_risk


def create_threat(data):
    """
    Create a threat and its associated indicator.

    This function:
    1. Validates the indicator syntax.
    2. Calculates a defensive risk score.
    3. Creates the threat record.
    4. Creates the indicator record.
    5. Returns the new threat ID.
    """

    required_fields = [
        "name",
        "category",
        "description",
        "severity",
        "confidence",
        "indicator_value"
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing_fields:
        raise ValueError(
            f"Missing required fields: {', '.join(missing_fields)}"
        )

    # Validate IOC syntax.
    indicator = validate_indicator(
        data["indicator_value"]
    )

    if not indicator["valid"]:
        raise ValueError(
            indicator["validation_notes"]
        )

    # Calculate defensive risk.
    risk = calculate_risk(
        severity=data["severity"],
        confidence=int(data["confidence"]),
        recency=int(data.get("recency", 70)),
        frequency=int(data.get("frequency", 50)),
        source_reliability=data.get(
            "source_reliability",
            "B"
        ),
        correlation=int(
            data.get("correlation", 50)
        )
    )

    now = datetime.utcnow().isoformat()

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # Create threat.
        cursor.execute(
            """
            INSERT INTO threats (
                name,
                category,
                description,
                severity,
                confidence,
                risk_score,
                status,
                source,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["name"],
                data["category"],
                data["description"],
                data["severity"],
                int(data["confidence"]),
                risk["score"],
                "NEW",
                data.get("source", "Internal"),
                now,
                now
            )
        )

        threat_id = cursor.lastrowid

        # Create associated indicator.
        cursor.execute(
            """
            INSERT INTO indicators (
                threat_id,
                indicator_type,
                indicator_value,
                normalized_value,
                validation_status,
                validation_notes,
                first_seen,
                last_seen
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                threat_id,
                indicator["indicator_type"],
                data["indicator_value"],
                indicator["normalized_value"],
                "VALID",
                indicator["validation_notes"],
                now,
                now
            )
        )

        connection.commit()

        return threat_id

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()