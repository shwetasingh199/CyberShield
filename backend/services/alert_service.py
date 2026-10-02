from datetime import datetime

from backend.core.database import get_connection


def create_alert_if_required(
    threat_id,
    threat_name,
    severity,
    risk_score,
    description
):
    """
    Create an alert for a high-risk threat.

    Alerts are created when the risk score is 61 or higher.
    Existing OPEN or INVESTIGATING alerts are not duplicated.
    """

    # Only create alerts for high-risk threats.
    if risk_score < 61:
        return None

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Check whether an active alert already exists.
        cursor.execute(
            """
            SELECT id
            FROM alerts
            WHERE threat_id = ?
            AND status IN ('OPEN', 'INVESTIGATING')
            """,
            (threat_id,)
        )

        existing = cursor.fetchone()

        if existing:
            return existing["id"]

        now = datetime.utcnow().isoformat()

        cursor.execute(
            """
            INSERT INTO alerts (
                threat_id,
                title,
                severity,
                status,
                description,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                threat_id,
                f"High-risk threat: {threat_name}",
                severity,
                "OPEN",
                description,
                now
            )
        )

        alert_id = cursor.lastrowid

        connection.commit()

        return alert_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()