def calculate_risk(
    severity,
    confidence,
    recency,
    frequency,
    source_reliability,
    correlation
):

    severity_values = {
        "INFORMATIONAL": 10,
        "LOW": 30,
        "MEDIUM": 50,
        "HIGH": 75,
        "CRITICAL": 95
    }

    source_values = {
        "A": 95,
        "B": 80,
        "C": 60,
        "D": 40
    }

    severity_score = severity_values.get(
        severity.upper(),
        10
    )

    source_score = source_values.get(
        source_reliability.upper(),
        40
    )

    score = (
        severity_score * 0.30 +
        confidence * 0.25 +
        recency * 0.15 +
        frequency * 0.10 +
        source_score * 0.10 +
        correlation * 0.10
    )

    score = round(
        max(0, min(score, 100))
    )

    return {
        "score": score,
        "classification": classify_risk(score)
    }


def classify_risk(score):

    if score <= 20:
        return "INFORMATIONAL"

    if score <= 40:
        return "LOW"

    if score <= 60:
        return "MEDIUM"

    if score <= 80:
        return "HIGH"

    return "CRITICAL"