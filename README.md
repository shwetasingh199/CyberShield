# 🛡️ CyberShield

### Cybersecurity Awareness & Threat Intelligence Platform

CyberShield is a defensive cybersecurity platform designed to help security teams, students, and organizations **validate indicators of compromise, correlate threat intelligence, assess risk, generate security alerts, track vulnerabilities, and improve security awareness** through an integrated web-based interface.

The project is designed around a simplified Security Operations Center (SOC) workflow:

> **Collect → Validate → Enrich → Correlate → Assess Risk → Generate Alerts → Investigate → Explain**

CyberShield combines threat intelligence, vulnerability management, IOC investigation, risk assessment, alert management, and cybersecurity awareness training into a single platform.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [SOC Workflow](#-soc-workflow)
- [Platform Architecture](#-platform-architecture)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Core Modules](#-core-modules)
- [Threat Intelligence](#-threat-intelligence)
- [IOC Investigation](#-ioc-investigation)
- [Risk Assessment](#-risk-assessment)
- [Alert Management](#-alert-management)
- [Vulnerability Management](#-vulnerability-management)
- [Security Awareness](#-security-awareness)
- [API Overview](#-api-overview)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [Database Seeding](#-database-seeding)
- [Testing](#-testing)
- [Security & Defensive Scope](#-security--defensive-scope)
- [Future Enhancements](#-future-enhancements)
- [Project Goals](#-project-goals)
- [Author](#-author)
- [License](#-license)

---

# 🔎 Overview

Modern security teams need to process large amounts of security information such as:

- IP addresses
- Domains
- URLs
- File hashes
- Email addresses
- CVE identifiers
- Security alerts
- Vulnerability records
- User-reported suspicious activity

CyberShield provides a centralized platform for working with these security artifacts in a controlled and defensive environment.

Instead of simply displaying raw data, CyberShield implements a security workflow that transforms an indicator into useful security context.

For example:

User submits IOC
       ↓
Indicator validation
       ↓
Normalization
       ↓
Local threat intelligence correlation
       ↓
Risk calculation
       ↓
Threat classification
       ↓
Alert generation
       ↓
Security explanation

## 🚀 Key Features

## Screenshots
<img width="1892" height="893" alt="P1 O s1" src="https://github.com/user-attachments/assets/b2e5b10a-5e6b-4f8b-888b-b96317eb4da0" />
<img width="1881" height="876" alt="P1 O s2" src="https://github.com/user-attachments/assets/20c694a1-5541-47d9-aaac-6405dbd45315" />
<img width="1872" height="887" alt="P1 O s3" src="https://github.com/user-attachments/assets/46f5a404-95a7-47cc-ae71-82660bc4b96c" />
<img width="1892" height="882" alt="P1 O s4" src="https://github.com/user-attachments/assets/c1486f60-c1f6-4ad7-94ec-4a4401bc2828" />
<img width="1908" height="825" alt="P1 O s5" src="https://github.com/user-attachments/assets/50e0d475-dd94-40de-b5de-1e6a3a96dc96" />
<img width="1852" height="878" alt="P1 O s6" src="https://github.com/user-attachments/assets/f7c7a2f9-a38f-4471-aab3-e36c84cc82d7" />
<img width="1866" height="862" alt="P1 O s7" src="https://github.com/user-attachments/assets/7cf4b440-5df9-4ce6-a6f3-4f64d17dc1ae" />

## 🔍 Threat Intelligence

CyberShield allows security analysts to manage and investigate threat intelligence records.

Supported indicator types include:

IPv4 / IPv6 addresses
Domains
URLs
MD5 hashes
SHA-1 hashes
SHA-256 hashes
Email addresses
CVE identifiers

Each indicator is validated before being stored or investigated.

## 🧪 Indicator Validation

The platform performs local syntax validation and normalization.

Examples:

192.168.1.10
example.com
https://example.com/login
d41d8cd98f00b204e9800998ecf8427e
CVE-2024-0001
security@example.com

The validator identifies the indicator type and produces validation information.

Example response:

{
    "valid": true,
    "indicator_type": "DOMAIN",
    "normalized_value": "example.com",
    "validation_notes": "Valid domain syntax. No DNS lookup was performed."
}

CyberShield intentionally avoids automatically contacting submitted domains or IP addresses.

## 🕵️ IOC Investigation

The IOC Investigation module provides a controlled investigation workflow.

An analyst can enter an indicator and CyberShield will:

Validate the indicator.
Normalize the value.
Search the local threat-intelligence database.
Identify matching threat records.
Display severity.
Display risk score.
Display threat category.
Display investigation status.
Provide relevant MITRE ATT&CK context where available.

Example workflow:

IOC
 │
 ├── Validate
 │
 ├── Normalize
 │
 ├── Local Database Search
 │
 ├── Threat Correlation
 │
 ├── Risk Assessment
 │
 └── ATT&CK Context

No external network request is required for local IOC investigation.

## ⚠️ Risk Assessment

CyberShield calculates a risk score using multiple security factors.

The current risk model considers:

Factor	Weight
Severity	30%
Confidence	25%
Recency	15%
Frequency	10%
Source Reliability	10%
Correlation	10%

The resulting score is normalized to a range of:

0 – 100

Risk classification:

Score	Classification
0–20	INFORMATIONAL
21–40	LOW
41–60	MEDIUM
61–80	HIGH
81–100	CRITICAL

This allows threat records to be prioritized using a consistent scoring model.

## 🚨 Alert Management

CyberShield can automatically generate alerts when a threat reaches a high-risk threshold.

Current behavior:

Risk Score < 61
      ↓
No high-risk alert

Risk Score >= 61
      ↓
Generate Alert

Alerts can have statuses such as:

OPEN
INVESTIGATING
RESOLVED
FALSE_POSITIVE

The system also prevents duplicate active alerts for the same threat.

## 🛡️ Vulnerability Management

The Vulnerability Center provides a dedicated interface for vulnerability records.

Each vulnerability can contain:

CVE identifier
Vulnerability title
Severity
CVSS score
Asset criticality
Exposure
Exploitation evidence
Remediation guidance
Current status

Example vulnerability workflow:

Vulnerability
      ↓
Severity Assessment
      ↓
Asset Criticality
      ↓
Exposure
      ↓
Exploitation Evidence
      ↓
Remediation Tracking

The vulnerability dashboard provides summary information including:

Total vulnerabilities
Open vulnerabilities
Critical vulnerabilities
Vulnerabilities with exploitation evidence

## 📚 Cybersecurity Awareness Center

CyberShield is not limited to security analysts.

The Awareness Center provides security education for users.

Current training areas include:

Phishing Awareness

Learn how to identify:

Suspicious emails
Unexpected links
Credential harvesting attempts
Impersonation attempts
Password & Authentication Security

Covers:

Strong passwords
Unique passwords
Password managers
Multi-factor authentication
Safe Web Browsing

Covers:

Suspicious websites
Unsafe downloads
Browser warnings
Secure browsing practices
Social Engineering Defense

Explains common manipulation techniques involving:

Urgency
Authority
Trust
Pressure
Incident Reporting

Teaches users how to report suspicious security activity through an organization's security process.

## 🧠 Security Awareness Quiz

The platform includes an interactive security quiz.

The workflow is:

Question
   ↓
User Answer
   ↓
Answer Validation
   ↓
Score Calculation
   ↓
Percentage
   ↓
Security Recommendation

Example result:

5 / 6 correct
83.33%

Strong security awareness.
Continue practicing with advanced scenarios.

Quiz results are stored locally for future analysis.

## 📊 Security Dashboard

The CyberShield dashboard provides a centralized SOC-style overview.

The dashboard includes:

Threat Metrics
Total threats
Active alerts
High-risk threats
Critical vulnerabilities
Investigation activity
Threat Activity

Threats can be viewed according to severity:

CRITICAL
HIGH
MEDIUM
LOW
INFORMATIONAL
Threat Categories

Examples include:

PHISHING
MALWARE
RANSOMWARE
CREDENTIAL_THREAT
WEB_THREAT
NETWORK_THREAT
VULNERABILITY
SOCIAL_ENGINEERING
DATA_EXPOSURE
ACCOUNT_SECURITY
Recent Threat Intelligence

The dashboard displays recent threat records including:

Threat name
Category
Severity
Risk score
Status
Alert Queue

Security alerts are presented separately so that analysts can quickly identify records requiring investigation.

## 🏗️ Platform Architecture

CyberShield follows a layered architecture.

┌───────────────────────────────────────────┐
│              Web Frontend                 │
│                                           │
│ Dashboard │ Investigation │ Awareness     │
│ Vulnerabilities                           │
└─────────────────────┬─────────────────────┘
                      │
                      │ HTTP / JSON
                      ▼
┌───────────────────────────────────────────┐
│              Flask REST API               │
│                                           │
│ Threat Routes                             │
│ Indicator Routes                          │
│ Investigation Routes                      │
│ Alert Routes                              │
│ Vulnerability Routes                      │
│ Awareness Routes                          │
│ Dashboard Routes                           │
└─────────────────────┬─────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────┐
│             Security Services             │
│                                           │
│ Indicator Validation                      │
│ Threat Management                         │
│ Risk Assessment                           │
│ Correlation                               │
│ Alert Generation                          │
│ Vulnerability Management                  │
│ Awareness Management                      │
└─────────────────────┬─────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────┐
│                SQLite                     │
│                                           │
│ Threats                                   │
│ Indicators                               │
│ Alerts                                   │
│ Vulnerabilities                           │
│ Awareness Modules                         │
│ Quiz Results                              │
└───────────────────────────────────────────┘

## 🧰 Technology Stack
Backend
Python
Flask
SQLite
python-dotenv
Frontend
HTML5
CSS3
JavaScript
Fetch API
Testing
Pytest
Development
Git
GitHub
Python Virtual Environment

## 📁 Project Structure
CyberShield/
│
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── threat_routes.py
│   │   ├── indicator_routes.py
│   │   ├── alert_routes.py
│   │   ├── vulnerability_routes.py
│   │   ├── awareness_routes.py
│   │   └── dashboard_routes.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── constants.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── indicator_service.py
│   │   ├── threat_service.py
│   │   ├── enrichment_service.py
│   │   ├── risk_service.py
│   │   ├── correlation_service.py
│   │   ├── alert_service.py
│   │   ├── attack_service.py
│   │   ├── vulnerability_service.py
│   │   └── awareness_service.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── validators.py
│
├── frontend/
│   ├── index.html
│   ├── investigation.html
│   ├── awareness.html
│   ├── vulnerabilities.html
│   │
│   ├── css/
│   │   ├── main.css
│   │   ├── dashboard.css
│   │   └── investigation.css
│   │
│   └── js/
│       ├── api.js
│       ├── dashboard.js
│       ├── investigation.js
│       ├── awareness.js
│       └── vulnerabilities.js
│
├── data/
│   ├── cyber_shield.db
│   ├── seed_threats.py
│   ├── seed_vulnerabilities.py
│   └── seed_awareness.py
│
├── awareness/
│   ├── modules.json
│   └── quiz.json
│
├── tests/
│   ├── test_indicators.py
│   ├── test_risk.py
│   ├── test_threats.py
│   ├── test_alerts.py
│   └── test_api.py
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── SOC_WORKFLOW.md
│   ├── THREAT_MODEL.md
│   ├── API.md
│   └── PROJECT_GUIDE.md
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

## 🔌 API Overview

CyberShield exposes REST-style API endpoints.

Health Check
GET /health

Example response:

{
    "status": "operational",
    "application": "CyberShield"
}
Threat Intelligence
Get Threats
GET /api/threats

Optional filters:

/api/threats?category=PHISHING
/api/threats?severity=HIGH
Create Threat
POST /api/threats

Example:

{
    "name": "Suspicious Credential Phishing Campaign",
    "category": "PHISHING",
    "description": "Suspicious credential harvesting activity.",
    "severity": "HIGH",
    "confidence": 90,
    "indicator_value": "example.com"
}
Indicator Validation
POST /api/indicators/validate

Example:

{
    "value": "example.com"
}
Vulnerabilities
Get Vulnerabilities
GET /api/vulnerabilities

Filtering:

/api/vulnerabilities?severity=CRITICAL
/api/vulnerabilities?status=OPEN
Vulnerability Summary
GET /api/vulnerabilities/summary
Awareness
Get Awareness Modules
GET /api/awareness/modules
Get Quiz
GET /api/awareness/quiz
Submit Quiz
POST /api/awareness/quiz/submit

Example:

{
    "score": 5,
    "total": 6
}

## 💻 Installation
1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/CyberShield.git
cd CyberShield
2. Create a Virtual Environment
Windows
python -m venv .venv

Activate it:

.venv\Scripts\activate
Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt

## ⚙️ Configuration

Create a .env file in the project root.

Example:

APP_NAME=CyberShield
APP_ENV=development

SECRET_KEY=change-this-secret-key
API_KEY=cybershield-demo-key

DATABASE_PATH=data/cyber_shield.db
Important

Do not commit .env to GitHub.

The repository should contain:

.env.example

instead of your real .env.

## 🗄️ Database Initialization

CyberShield uses SQLite for local development.

The database is automatically initialized when the Flask application starts.

The following tables are created:

threats
indicators
alerts
analyst_notes
vulnerabilities
awareness_modules
quiz_results

## 🌱 Database Seeding

CyberShield includes seed scripts for demonstration and development.

Threat Intelligence
python data\seed_threats.py
Vulnerabilities
python data\seed_vulnerabilities.py
Awareness Modules
python data\seed_awareness.py

These scripts create local demonstration records so the dashboard can be evaluated without requiring external threat-intelligence services.

## ▶️ Running the Application

From the project root:

python -m backend.app

The Flask application will start on:

http://127.0.0.1:5000

Open the dashboard in a browser:

http://127.0.0.1:5000/

## 🖥️ Application Pages
Dashboard
/

Central SOC-style overview of:

Threats
Alerts
Risk
Vulnerabilities
Investigations
IOC Investigation
/investigation.html

Used for:

Indicator validation
Local threat correlation
Risk context
ATT&CK context
Vulnerability Center
/vulnerabilities.html

Used for:

Vulnerability filtering
Severity analysis
CVSS review
Exposure review
Remediation tracking
Awareness Center
/awareness.html

Used for:

Security awareness modules
Cybersecurity education
Interactive quizzes
Security knowledge assessment

## 🧪 Testing

Run the test suite with:

pytest

Tests are intended to validate important components including:

Indicator validation
Risk calculation
Threat creation
Alert generation
API behavior

## 🔐 Security & Defensive Scope

CyberShield is intentionally designed as a defensive cybersecurity project.

The platform does not perform offensive security operations.

CyberShield does NOT:
Execute malware
Deliver malicious payloads
Exploit vulnerabilities
Perform unauthorized penetration testing
Scan arbitrary public networks
Perform port scanning
Perform DNS reconnaissance
Automatically contact suspicious domains
Intercept browser traffic
Steal credentials
Extract passwords
Deploy persistence mechanisms
Modify remote systems

Instead, the platform focuses on:

Validation
Correlation
Risk Assessment
Alerting
Investigation
Vulnerability Management
Security Awareness

This makes the project suitable for educational environments, defensive security portfolios, and controlled demonstrations.

## 🧩 Design Philosophy

CyberShield follows several design principles.

1. Defensive by Design

Security functionality is focused on identifying, understanding, and managing potential threats.

2. Local-First Investigation

IOC investigation can operate against local threat intelligence without automatically contacting external infrastructure.

3. Explainable Risk

Risk scores are generated from explicit factors instead of being treated as unexplained black-box predictions.

4. Separation of Responsibilities

The project separates:

API
Business Logic
Database
Frontend
Security Services
Seed Data
Testing
Documentation

This improves maintainability and makes the architecture easier to extend.

5. Human-in-the-Loop Security

CyberShield provides information and security context to an analyst rather than attempting to automatically make irreversible security decisions.

## 🔄 SOC Workflow

The core CyberShield workflow is:

┌──────────────┐
│    Collect   │
└──────┬───────┘
       ↓
┌──────────────┐
│   Validate   │
└──────┬───────┘
       ↓
┌──────────────┐
│   Enrich     │
└──────┬───────┘
       ↓
┌──────────────┐
│  Correlate   │
└──────┬───────┘
       ↓
┌──────────────┐
│ Assess Risk  │
└──────┬───────┘
       ↓
┌──────────────┐
│ Generate     │
│ Alerts       │
└──────┬───────┘
       ↓
┌──────────────┐
│ Investigate  │
└──────┬───────┘
       ↓
┌──────────────┐
│   Explain    │
└──────────────┘

## 🎯 Project Goals

CyberShield was developed to demonstrate practical understanding of:

Cybersecurity fundamentals
Threat intelligence
Indicators of compromise
IOC validation
Risk scoring
Threat correlation
Security alerting
Vulnerability management
Security awareness
REST API development
Backend architecture
Database design
Frontend development
Secure software practices
Defensive SOC workflows

The project is intended to demonstrate how multiple cybersecurity concepts can be integrated into one practical application.

## 🔮 Future Enhancements

Potential future versions may include additional defensive capabilities.

Endpoint Telemetry

A controlled local endpoint component could collect:

Operating-system information
Local asset information
File hashes
Security events
Process inventory
Local configuration information

No remote exploitation or unauthorized access would be required.

Threat Intelligence Enrichment

Future versions could support carefully controlled integrations with reputable threat-intelligence sources.

Potential enrichment could include:

IOC Reputation
Threat Actor Context
Malware Family Information
Domain Reputation
IP Reputation
CVE Information

External requests should remain explicit, controlled, and safe.

MITRE ATT&CK Expansion

The current implementation provides basic ATT&CK context.

Future versions could expand coverage to include:

More tactics
More techniques
Sub-techniques
Detection guidance
Defensive mitigations
Advanced Correlation

Future correlation could connect:

IOC
 ↓
Threat
 ↓
Vulnerability
 ↓
Asset
 ↓
Alert
 ↓
Incident

This would provide a more complete SOC investigation workflow.

Endpoint Detection & Response Concepts

A future defensive extension could provide controlled local telemetry similar to an introductory EDR workflow:

Endpoint Event
      ↓
Event Normalization
      ↓
Detection Rule
      ↓
Risk Assessment
      ↓
Alert
      ↓
Analyst Investigation

The implementation would remain focused on defensive monitoring rather than offensive capabilities.

## 📈 Example SOC Scenario

A security analyst receives a suspicious domain:

example-suspicious-domain.com

The analyst enters the domain into CyberShield.

Step 1 — Validation

CyberShield verifies that the value has valid domain syntax.

Step 2 — Normalization

The domain is normalized for consistent comparison.

Step 3 — Correlation

The system searches local threat-intelligence records.

Step 4 — Risk Assessment

The associated threat record is evaluated using:

Severity
Confidence
Recency
Frequency
Source Reliability
Correlation
Step 5 — Alerting

If the resulting risk score reaches the configured high-risk threshold, an alert can be generated.

Step 6 — Investigation

The analyst reviews:

Threat description
Indicator
Category
Severity
Risk score
Status
ATT&CK context
Step 7 — Response

The analyst can use the information to support the organization's existing security-response process.

## 🧑‍💻 Development

The project is organized so that individual components can be developed and tested independently.

For example:

Indicator validation
        ↓
Threat service
        ↓
Risk service
        ↓
Alert service
        ↓
API
        ↓
Frontend

This structure makes it easier to extend the platform without tightly coupling every component.

## 📌 Project Status

CyberShield is an actively developed cybersecurity portfolio project.

Current implemented areas include:

 Flask backend
 SQLite database
 Threat intelligence records
 IOC validation
 Risk scoring
 Threat correlation
 Alert generation
 IOC investigation interface
 Vulnerability management interface
 Vulnerability summary
 Security awareness modules
 Security awareness quiz
 Quiz scoring
 SOC-style dashboard
 Defensive security scope
 Advanced endpoint telemetry
 Expanded ATT&CK coverage
 Advanced threat-intelligence enrichment
 Incident management workflow
 Authentication and role-based access control
 Production deployment configuration
 
## 🛠️ Troubleshooting
Flask does not start

Make sure the virtual environment is activated:

.venv\Scripts\activate

Then install dependencies:

pip install -r requirements.txt

Start the application:

python -m backend.app
Database is empty

Run the seed scripts:

python data\seed_threats.py
python data\seed_vulnerabilities.py
python data\seed_awareness.py

Then restart Flask if necessary.

Backend module cannot be found

Run Python commands from the project root:

cd "C:\Users\shwet\OneDrive\Desktop\CyberShield"

Then use:

python -m backend.app

For seed scripts, ensure the project root is available on Python's module path.

## 🤝 Contributing

Contributions and suggestions are welcome.

A typical contribution workflow is:

Fork
 ↓
Create Feature Branch
 ↓
Implement Change
 ↓
Run Tests
 ↓
Commit
 ↓
Push
 ↓
Create Pull Request

Before submitting changes:

pytest

should complete successfully.

## 📜 License

This project is intended as a cybersecurity education and portfolio project.

A specific open-source license can be added before public distribution.

## 👨‍💻 Author

Shweta
CyberShield

Cybersecurity Awareness & Threat Intelligence Platform
Analyst investigation
       ↓
Security explanation
