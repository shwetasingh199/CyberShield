from backend.core.database import get_connection


def find_related_threats(threat_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            t.id,
            t.name,
            t.category,
            t.severity,
            t.risk_score,
            i.indicator_type,
            i.indicator_value
        FROM threats t
        LEFT JOIN indicators i
            ON t.id = i.threat_id
        WHERE t.id != ?
        AND t.category = (
            SELECT category
            FROM threats
            WHERE id = ?
        )
        ORDER BY t.risk_score DESC
        LIMIT 10
        """,
        (threat_id, threat_id)
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]