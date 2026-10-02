from flask import Blueprint, request, jsonify

from backend.core.database import get_connection
from backend.services.threat_service import create_threat


threat_api = Blueprint(
    "threat_api",
    __name__,
    url_prefix="/api/threats"
)


@threat_api.get("")
def get_threats():

    connection = get_connection()

    cursor = connection.cursor()

    category = request.args.get("category")
    severity = request.args.get("severity")

    query = """
        SELECT *
        FROM threats
        WHERE 1 = 1
    """

    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if severity:
        query += " AND severity = ?"
        params.append(severity)

    query += """
        ORDER BY risk_score DESC
        LIMIT 100
    """

    cursor.execute(
        query,
        params
    )

    threats = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return jsonify(threats)


@threat_api.post("")
def add_threat():

    data = request.get_json()

    required = [
        "name",
        "category",
        "description",
        "severity",
        "confidence",
        "indicator_value"
    ]

    missing = [
        field
        for field in required
        if field not in data
    ]

    if missing:
        return jsonify({
            "error": "Missing fields",
            "fields": missing
        }), 400

    try:

        threat_id = create_threat(data)

        return jsonify({
            "message": "Threat created.",
            "threat_id": threat_id
        }), 201

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400