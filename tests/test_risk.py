"""
Automated tests for the defensive CTI dashboard.
"""

import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT_DIR)
    )


from backend.services.ioc_validator import (
    validate_indicator
)

from backend.services.risk_engine import (
    calculate_threat_risk,
    calculate_confidence,
    calculate_vulnerability_priority,
    classify_risk
)

from backend.services.attack_mapper import (
    map_threat_to_attack
)

from backend.services.alert_engine import (
    generate_threat_alert
)

from backend.services.correlation_engine import (
    correlate_threats,
    correlate_alerts
)


def test_valid_ipv4():
    result = validate_indicator(
        "192.0.2.25"
    )

    assert result["valid"] is True


def test_invalid_ipv4():
    result = validate_indicator(
        "999.999.999.999"
    )

    assert result["valid"] is False


def test_valid_ipv6():
    result = validate_indicator(
        "2001:db8::1"
    )

    assert result["valid"] is True


def test_valid_domain():
    result = validate_indicator(
        "example.com"
    )

    assert result["valid"] is True


def test_invalid_domain():
    result = validate_indicator(
        "not a domain"
    )

    assert result["valid"] is False


def test_valid_url():
    result = validate_indicator(
        "https://example.com/demo"
    )

    assert result["valid"] is True


def test_valid_md5():
    result = validate_indicator(
        "a" * 32
    )

    assert result["valid"] is True


def test_valid_sha1():
    result = validate_indicator(
        "a" * 40
    )

    assert result["valid"] is True


def test_valid_sha256():
    result = validate_indicator(
        "a" * 64
    )

    assert result["valid"] is True


def test_valid_cve():
    result = validate_indicator(
        "CVE-2026-12345"
    )

    assert result["valid"] is True


def test_invalid_cve():
    result = validate_indicator(
        "CVE-ABC-123"
    )

    assert result["valid"] is False


def test_risk_calculation():
    result = calculate_threat_risk(
        severity="HIGH",
        confidence=90,
        recency=90,
        observation_frequency=5,
        source_reliability="A",
        context=80
    )

    assert 0 <= result["risk_score"] <= 100


def test_risk_classification():
    assert classify_risk(90) == "CRITICAL"


def test_confidence_calculation():
    result = calculate_confidence(
        source_reliability="A",
        corroboration=90,
        data_quality=90
    )

    assert result > 80


def test_source_reliability():
    high = calculate_confidence(
        source_reliability="A",
        corroboration=80,
        data_quality=80
    )

    low = calculate_confidence(
        source_reliability="D",
        corroboration=80,
        data_quality=80
    )

    assert high > low


def test_attack_mapping():
    result = map_threat_to_attack(
        "PHISHING"
    )

    assert result is not None

    assert result["tactic"] == "Initial Access"


def test_attack_mapping_unknown():
    result = map_threat_to_attack(
        "UNKNOWN"
    )

    assert result is None


def test_alert_generation():
    alert = generate_threat_alert(
        "THR-2026-0001",
        78,
        85
    )

    assert alert["threat_id"] == (
        "THR-2026-0001"
    )

    assert alert["severity"] == "HIGH"


def test_correlation():
    records = [
        {
            "campaign_id": "CAMP-001",
            "indicator_value": "example.com"
        },
        {
            "campaign_id": "CAMP-001",
            "indicator_value": "192.0.2.10"
        }
    ]

    clusters = correlate_threats(
        records
    )

    assert len(clusters) == 1

    assert clusters[0][
        "observation_count"
    ] == 2


def test_single_record_no_cluster():
    records = [
        {
            "campaign_id": "CAMP-001",
            "indicator_value": "example.com"
        }
    ]

    clusters = correlate_threats(
        records
    )

    assert clusters == []


def test_alert_correlation():
    alerts = [
        {
            "threat_id": "THR-1",
            "alert_type": "RISK"
        },
        {
            "threat_id": "THR-1",
            "alert_type": "RISK"
        }
    ]

    result = correlate_alerts(
        alerts
    )

    assert len(result) == 1

    assert result[0][
        "observation_count"
    ] == 2


def test_vulnerability_priority():
    score = calculate_vulnerability_priority(
        cvss_score=9.0,
        asset_criticality=90,
        exposure=90,
        exploitation_evidence=80,
        business_context=90
    )

    assert 0 <= score <= 100


def test_low_vulnerability_priority():
    score = calculate_vulnerability_priority(
        cvss_score=3.0,
        asset_criticality=20,
        exposure=10,
        exploitation_evidence=0,
        business_context=20
    )

    assert score < 50


def test_empty_indicator():
    result = validate_indicator("")

    assert result["valid"] is False


def test_none_indicator():
    result = validate_indicator(None)

    assert result["valid"] is False


def test_domain_normalization():
    result = validate_indicator(
        "EXAMPLE.COM"
    )

    assert result["normalized_value"] == (
        "example.com"
    )


def test_url_normalization():
    result = validate_indicator(
        "https://example.com/"
    )

    assert result["normalized_value"] == (
        "https://example.com"
    )


def test_cve_normalization():
    result = validate_indicator(
        "cve-2026-12345"
    )

    assert result["normalized_value"] == (
        "CVE-2026-12345"
    )


def test_hash_normalization():
    result = validate_indicator(
        "A" * 64
    )

    assert result["normalized_value"] == (
        "a" * 64
    )


def test_risk_range():
    result = calculate_threat_risk(
        severity="CRITICAL",
        confidence=100,
        recency=100,
        observation_frequency=100,
        source_reliability="A",
        context=100
    )

    assert result["risk_score"] <= 100


def test_confidence_range():
    result = calculate_confidence(
        "A",
        100,
        100
    )

    assert 0 <= result <= 100


def test_alert_low_severity():
    alert = generate_threat_alert(
        "THR-1",
        20,
        50
    )

    assert alert["severity"] == (
        "INFORMATIONAL"
    )


def test_alert_medium_severity():
    alert = generate_threat_alert(
        "THR-1",
        50,
        50
    )

    assert alert["severity"] == "MEDIUM"


def test_alert_critical_severity():
    alert = generate_threat_alert(
        "THR-1",
        95,
        95
    )

    assert alert["severity"] == "CRITICAL"


def test_alert_status():
    alert = generate_threat_alert(
        "THR-1",
        70,
        90
    )

    assert alert["status"] == "NEW"


def test_correlation_note():
    records = [
        {
            "campaign_id": "CAMP-2",
            "indicator_value": "example.com"
        },
        {
            "campaign_id": "CAMP-2",
            "indicator_value": "192.0.2.1"
        }
    ]

    clusters = correlate_threats(
        records
    )

    assert "correlation_note" in clusters[0]


def test_attack_mapping_note():
    result = map_threat_to_attack(
        "RANSOMWARE"
    )

    assert "mapping_note" in result


def test_indicator_type_ip():
    result = validate_indicator(
        "198.51.100.25"
    )

    assert result["indicator_type"] == (
        "IP ADDRESS"
    )


def test_indicator_type_url():
    result = validate_indicator(
        "https://example.com/test"
    )

    assert result["indicator_type"] == (
        "URL"
    )


def test_indicator_type_sha256():
    result = validate_indicator(
        "b" * 64
    )

    assert result["indicator_type"] == (
        "SHA-256 HASH"
    )


def test_indicator_type_cve():
    result = validate_indicator(
        "CVE-2026-99999"
    )

    assert result["indicator_type"] == (
        "CVE ID"
    )


def test_negative_risk_is_clamped():
    result = calculate_threat_risk(
        severity="INFORMATIONAL",
        confidence=0,
        recency=0,
        observation_frequency=0,
        source_reliability="D",
        context=0
    )

    assert result["risk_score"] >= 0