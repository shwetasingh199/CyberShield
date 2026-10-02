import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.database import (
    get_connection,
    initialize_database
)


VULNERABILITIES = [
    {
        "cve_id": "CVE-2024-3094",
        "title": "Simulated Critical Library Vulnerability",
        "severity": "CRITICAL",
        "cvss": 10.0,
        "asset_criticality": 95,
        "exposure": 90,
        "exploitation_evidence": 1,
        "remediation": "Upgrade affected dependency and verify deployment integrity.",
        "status": "OPEN"
    },
    {
        "cve_id": "CVE-2024-21413",
        "title": "Simulated Email Client Security Vulnerability",
        "severity": "HIGH",
        "cvss": 8.1,
        "asset_criticality": 85,
        "exposure": 75,
        "exploitation_evidence": 1,
        "remediation": "Apply vendor security updates and review affected endpoints.",
        "status": "IN_REVIEW"
    },
    {
        "cve_id": "CVE-2023-34362",
        "title": "Simulated Web Application Vulnerability",
        "severity": "HIGH",
        "cvss": 8.8,
        "asset_criticality": 80,
        "exposure": 70,
        "exploitation_evidence": 0,
        "remediation": "Patch affected application and validate configuration.",
        "status": "OPEN"
    },
    {
        "cve_id": "CVE-2024-0001",
        "title": "Simulated Authentication Weakness",
        "severity": "MEDIUM",
        "cvss": 6.5,
        "asset_criticality": 70,
        "exposure": 55,
        "exploitation_evidence": 0,
        "remediation": "Apply security update and strengthen authentication controls.",
        "status": "IN_REVIEW"
    },
    {
        "cve_id": "CVE-2024-0002",
        "title": "Simulated Information Disclosure",
        "severity": "LOW",
        "cvss": 3.7,
        "asset_criticality": 40,
        "exposure": 25,
        "exploitation_evidence": 0,
        "remediation": "Apply recommended configuration change during maintenance.",
        "status": "RESOLVED"
    }
]


def seed_vulnerabilities():
    initialize_database()

    connection = get_connection()

    try:
        existing = connection.execute(
            "SELECT COUNT(*) FROM vulnerabilities"
        ).fetchone()[0]

        if existing > 0:
            print(
                f"Vulnerability database already contains "
                f"{existing} records."
            )
            print("No new vulnerability records were inserted.")
            return

        for vulnerability in VULNERABILITIES:
            connection.execute(
                """
                INSERT INTO vulnerabilities (
                    cve_id,
                    title,
                    severity,
                    cvss,
                    asset_criticality,
                    exposure,
                    exploitation_evidence,
                    remediation,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    vulnerability["cve_id"],
                    vulnerability["title"],
                    vulnerability["severity"],
                    vulnerability["cvss"],
                    vulnerability["asset_criticality"],
                    vulnerability["exposure"],
                    vulnerability["exploitation_evidence"],
                    vulnerability["remediation"],
                    vulnerability["status"]
                )
            )

        connection.commit()

        print()
        print("====================================")
        print("Vulnerability Seed Complete")
        print("====================================")
        print(
            f"Vulnerabilities created: "
            f"{len(VULNERABILITIES)}"
        )

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    seed_vulnerabilities()