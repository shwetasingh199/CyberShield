from flask import Blueprint, jsonify, request

from backend.core.database import get_connection

from backend.services.indicator_service import (
    validate_indicator
)

from backend.services.correlation_service import (
    find_related_threats
)

from backend.services.attack_service import (
    map_threat_to_attack
)


investigation_api = Blueprint(
    "investigation_api",
    __name__,
    url_prefix="/api/investigation"
)


@investigation_api.get("/lookup")
def lookup():

    value = request.args.get(
        "value",
        ""
    ).strip()

    if not value:

        return jsonify({
            "error": "Indicator value is required."
        }), 400

    validation = validate_indicator(
        value
    )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            t.*,
            i.indicator_type,
            i.indicator_value,
            i.normalized_value,
            i.validation_status,
            i.validation_notes,
            i.first_seen,
            i.last_seen
        FROM indicators i
        JOIN threats t
            ON t.id = i.threat_id
        WHERE
            i.normalized_value = ?
            OR i.indicator_value = ?
        ORDER BY t.risk_score DESC
        LIMIT 20
        """,
        (
            validation["normalized_value"],
            value
        )
    )

    matches = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    for match in matches:

        match["attack_mapping"] = (
            map_threat_to_attack(
                match["category"]
            )
        )

        match["related_threats"] = (
            find_related_threats(
                match["id"]
            )
        )

    return jsonify({

        "validation": validation,

        "matches": matches,

        "network_activity_performed": False

    })