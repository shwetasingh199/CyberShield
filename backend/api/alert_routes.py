from flask import Blueprint, jsonify, request

from backend.core.database import get_connection


alert_api = Blueprint(
    "alert_api",
    __name__,
    url_prefix="/api/alerts"
)


@alert_api.get("")
def get_alerts():

    connection = get_connection()

    cursor = connection.cursor()

    status = request.args.get("status")

    query = """
        SELECT
            a.*,
            t.name AS threat_name,
            t.category AS threat_category,
            t.risk_score
        FROM alerts a
        LEFT JOIN threats t
            ON t.id = a.threat_id
        WHERE 1 = 1
    """

    params = []

    if status:

        query += """
            AND a.status = ?
        """

        params.append(status)

    query += """
        ORDER BY a.id DESC
        LIMIT 50
    """

    cursor.execute(
        query,
        params
    )

    alerts = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return jsonify(alerts)


@alert_api.patch("/<int:alert_id>")
def update_alert(alert_id):

    data = request.get_json(
        silent=True
    ) or {}

    status = data.get("status")

    allowed_statuses = {
        "OPEN",
        "INVESTIGATING",
        "RESOLVED",
        "FALSE_POSITIVE"
    }

    if status not in allowed_statuses:

        return jsonify({
            "error": "Invalid alert status."
        }), 400

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE alerts
        SET status = ?
        WHERE id = ?
        """,
        (
            status,
            alert_id
        )
    )

    connection.commit()

    changed = cursor.rowcount

    connection.close()

    if not changed:

        return jsonify({
            "error": "Alert not found."
        }), 404

    return jsonify({
        "message": "Alert updated.",
        "status": status
    })