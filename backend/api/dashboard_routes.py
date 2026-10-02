from flask import Blueprint, jsonify

from backend.core.database import get_connection


dashboard_api = Blueprint(
    "dashboard_api",
    __name__,
    url_prefix="/api/dashboard"
)


@dashboard_api.get("/stats")
def dashboard_stats():

    connection = get_connection()

    cursor = connection.cursor()

    def count(query):

        cursor.execute(query)

        return cursor.fetchone()["count"]

    total_threats = count(
        """
        SELECT COUNT(*) AS count
        FROM threats
        """
    )

    active_alerts = count(
        """
        SELECT COUNT(*) AS count
        FROM alerts
        WHERE status IN (
            'OPEN',
            'INVESTIGATING'
        )
        """
    )

    high_risk = count(
        """
        SELECT COUNT(*) AS count
        FROM threats
        WHERE risk_score >= 61
        """
    )

    vulnerabilities = count(
        """
        SELECT COUNT(*) AS count
        FROM vulnerabilities
        """
    )

    critical_vulnerabilities = count(
        """
        SELECT COUNT(*) AS count
        FROM vulnerabilities
        WHERE severity = 'CRITICAL'
        """
    )

    investigations = count(
        """
        SELECT COUNT(*) AS count
        FROM alerts
        WHERE status = 'INVESTIGATING'
        """
    )

    cursor.execute(
        """
        SELECT
            severity,
            COUNT(*) AS count
        FROM threats
        GROUP BY severity
        """
    )

    severity_rows = cursor.fetchall()

    threat_severity = {
        row["severity"]: row["count"]
        for row in severity_rows
    }

    cursor.execute(
        """
        SELECT
            category,
            COUNT(*) AS count
        FROM threats
        GROUP BY category
        ORDER BY count DESC
        LIMIT 8
        """
    )

    categories = [
        dict(row)
        for row in cursor.fetchall()
    ]

    cursor.execute(
        """
        SELECT
            id,
            name,
            category,
            severity,
            risk_score,
            status,
            created_at
        FROM threats
        ORDER BY id DESC
        LIMIT 8
        """
    )

    recent_threats = [
        dict(row)
        for row in cursor.fetchall()
    ]

    cursor.execute(
        """
        SELECT
            a.id,
            a.title,
            a.severity,
            a.status,
            a.created_at,
            t.name AS threat_name,
            t.risk_score
        FROM alerts a
        LEFT JOIN threats t
            ON t.id = a.threat_id
        ORDER BY a.id DESC
        LIMIT 8
        """
    )

    recent_alerts = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return jsonify({

        "total_threats": total_threats,

        "active_alerts": active_alerts,

        "high_risk_threats": high_risk,

        "vulnerabilities": vulnerabilities,

        "critical_vulnerabilities":
            critical_vulnerabilities,

        "investigations":
            investigations,

        "threat_severity":
            threat_severity,

        "categories":
            categories,

        "recent_threats":
            recent_threats,

        "recent_alerts":
            recent_alerts
    })