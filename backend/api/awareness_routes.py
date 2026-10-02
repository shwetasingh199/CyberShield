from flask import Blueprint, request, jsonify

from backend.services.awareness_service import (
    get_modules,
    get_quiz,
    submit_quiz
)


awareness_api = Blueprint(
    "awareness_api",
    __name__,
    url_prefix="/api/awareness"
)


@awareness_api.get("/modules")
def modules():
    return jsonify(
        get_modules()
    )


@awareness_api.get("/quiz")
def quiz():
    return jsonify(
        get_quiz()
    )


@awareness_api.post("/quiz/submit")
def submit():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required."
        }), 400

    if "score" not in data or "total" not in data:
        return jsonify({
            "error": "Score and total are required."
        }), 400

    try:
        result = submit_quiz(
            data["score"],
            data["total"]
        )

        return jsonify(result)

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400