"""
Local threat enrichment engine.

No external network calls are performed.
"""

import sqlite3


def enrich_indicator(db_path, indicator):
    """
    Search local SQLite data for an indicator and return enrichment.
    """

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row

    try:
        query = """
            SELECT *
            FROM threats
            WHERE indicator_value = ?
            ORDER BY last_seen DESC
        """

        rows = connection.execute(
            query,
            (indicator,)
        ).fetchall()

        if not rows:
            return {
                "found": False,
                "indicator": indicator,
                "records": []
            }

        records = [dict(row) for row in rows]

        categories = sorted({
            row["category"]
            for row in records
            if row.get("category")
        })

        related_indicators = sorted({
            row["indicator_value"]
            for row in records
            if row.get("indicator_value")
        })

        return {
            "found": True,
            "indicator": indicator,
            "indicator_type": records[0].get(
                "indicator_type"
            ),
            "first_seen": min(
                row["first_seen"]
                for row in records
            ),
            "last_seen": max(
                row["last_seen"]
                for row in records
            ),
            "categories": categories,
            "related_indicators": related_indicators,
            "records": records
        }

    finally:
        connection.close()