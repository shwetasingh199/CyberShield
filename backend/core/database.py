import sqlite3
from pathlib import Path

from backend.config import Config


def get_connection():
    database_path = Path(Config.DATABASE_PATH)

    database_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        database_path
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            severity TEXT NOT NULL,
            confidence INTEGER NOT NULL,
            risk_score INTEGER NOT NULL,
            status TEXT NOT NULL,
            source TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS indicators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            threat_id INTEGER,
            indicator_type TEXT NOT NULL,
            indicator_value TEXT NOT NULL,
            normalized_value TEXT NOT NULL,
            validation_status TEXT NOT NULL,
            validation_notes TEXT,
            first_seen TEXT,
            last_seen TEXT,
            FOREIGN KEY(threat_id)
                REFERENCES threats(id)
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            threat_id INTEGER,
            title TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(threat_id)
                REFERENCES threats(id)
        );

        CREATE TABLE IF NOT EXISTS analyst_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            threat_id INTEGER NOT NULL,
            analyst TEXT NOT NULL,
            note TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(threat_id)
                REFERENCES threats(id)
        );

        CREATE TABLE IF NOT EXISTS vulnerabilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cve_id TEXT NOT NULL,
            title TEXT NOT NULL,
            severity TEXT NOT NULL,
            cvss REAL NOT NULL,
            asset_criticality INTEGER NOT NULL,
            exposure INTEGER NOT NULL,
            exploitation_evidence INTEGER NOT NULL,
            remediation TEXT NOT NULL,
            status TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS awareness_modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            content TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            submitted_at TEXT NOT NULL
        );
    """)

    connection.commit()
    connection.close()