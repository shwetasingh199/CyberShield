ATTACK_MAPPINGS = {
    "PHISHING": {
        "tactic": "Initial Access",
        "technique_id": "T1566",
        "technique": "Phishing"
    },

    "PHISHING_LINK": {
        "tactic": "Initial Access",
        "technique_id": "T1566.002",
        "technique": "Spearphishing Link"
    },

    "PHISHING_ATTACHMENT": {
        "tactic": "Initial Access",
        "technique_id": "T1566.001",
        "technique": "Spearphishing Attachment"
    }
}


def map_threat_to_attack(category):

    category = category.upper()

    return ATTACK_MAPPINGS.get(
        category
    )