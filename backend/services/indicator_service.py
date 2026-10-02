import hashlib
import ipaddress
import re
from urllib.parse import urlparse


CVE_PATTERN = re.compile(
    r"^CVE-\d{4}-\d{4,7}$",
    re.IGNORECASE
)

EMAIL_PATTERN = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)

DOMAIN_PATTERN = re.compile(
    r"^(?=.{1,253}$)"
    r"(?:[a-zA-Z0-9]"
    r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,63}$"
)


def validate_indicator(value):

    if not value or not value.strip():
        return {
            "valid": False,
            "indicator_type": None,
            "normalized_value": None,
            "validation_notes": "Indicator is empty."
        }

    value = value.strip()

    # IPv4 / IPv6
    try:
        ipaddress.ip_address(value)

        return {
            "valid": True,
            "indicator_type": "IP",
            "normalized_value": value,
            "validation_notes": "Valid IP address syntax."
        }

    except ValueError:
        pass

    # SHA256
    if re.fullmatch(r"[A-Fa-f0-9]{64}", value):
        return {
            "valid": True,
            "indicator_type": "SHA256",
            "normalized_value": value.lower(),
            "validation_notes": "Valid SHA-256 format."
        }

    # SHA1
    if re.fullmatch(r"[A-Fa-f0-9]{40}", value):
        return {
            "valid": True,
            "indicator_type": "SHA1",
            "normalized_value": value.lower(),
            "validation_notes": "Valid SHA-1 format."
        }

    # MD5
    if re.fullmatch(r"[A-Fa-f0-9]{32}", value):
        return {
            "valid": True,
            "indicator_type": "MD5",
            "normalized_value": value.lower(),
            "validation_notes": "Valid MD5 format."
        }

    # CVE
    if CVE_PATTERN.fullmatch(value):
        return {
            "valid": True,
            "indicator_type": "CVE",
            "normalized_value": value.upper(),
            "validation_notes": "Valid CVE identifier syntax."
        }

    # Email
    if EMAIL_PATTERN.fullmatch(value):
        return {
            "valid": True,
            "indicator_type": "EMAIL",
            "normalized_value": value.lower(),
            "validation_notes": "Valid email syntax."
        }

    # URL
    parsed = urlparse(value)

    if parsed.scheme in ("http", "https") and parsed.netloc:

        return {
            "valid": True,
            "indicator_type": "URL",
            "normalized_value": value,
            "validation_notes": "Valid HTTP/HTTPS URL syntax. No network request was performed."
        }

    # Domain
    if DOMAIN_PATTERN.fullmatch(value):

        return {
            "valid": True,
            "indicator_type": "DOMAIN",
            "normalized_value": value.lower(),
            "validation_notes": "Valid domain syntax. No DNS lookup was performed."
        }

    return {
        "valid": False,
        "indicator_type": None,
        "normalized_value": value,
        "validation_notes": "Unsupported or invalid indicator syntax."
    }