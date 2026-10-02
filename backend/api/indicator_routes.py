from flask import Blueprint, request, jsonify

from backend.services.indicator_service import (
    validate_indicator
)


indicator_api = Blueprint(
    "indicator_api",
    __name__,
    url_prefix="/api/indicators"
)


@indicator_api.post("/validate")
def validate():

    data = request.get_json()

    if not data or "value" not in data:
        return jsonify({
            "error": "Indicator value is required."
        }), 400

    result = validate_indicator(
        data["value"]
    )

    return jsonify(result)