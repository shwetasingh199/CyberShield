from pathlib import Path

from flask import Flask, send_from_directory

from backend.config import Config
from backend.core.database import initialize_database

from backend.api.threat_routes import threat_api
from backend.api.indicator_routes import indicator_api
from backend.api.dashboard_routes import dashboard_api
from backend.api.vulnerability_routes import vulnerability_api
from backend.api.awareness_routes import awareness_api


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


def create_app():
    app = Flask(
        __name__,
        static_folder=str(FRONTEND_DIR),
        static_url_path=""
    )

    app.config.from_object(Config)

    initialize_database()

    app.register_blueprint(threat_api)
    app.register_blueprint(indicator_api)
    app.register_blueprint(dashboard_api)
    app.register_blueprint(vulnerability_api)
    app.register_blueprint(awareness_api)

    @app.get("/")
    def home():
        return send_from_directory(
            str(FRONTEND_DIR),
            "index.html"
        )

    @app.get("/health")
    def health():
        return {
            "status": "operational",
            "application": "CyberShield"
        }

    @app.get("/<path:filename>")
    def frontend_files(filename):
        if filename.startswith("api/"):
            return {
                "error": "API endpoint not found."
            }, 404

        return send_from_directory(
            str(FRONTEND_DIR),
            filename
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )