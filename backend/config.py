import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_NAME = os.getenv("APP_NAME", "CyberShield")
    APP_ENV = os.getenv("APP_ENV", "development")

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret"
    )

    API_KEY = os.getenv(
        "API_KEY",
        "cybershield-demo-key"
    )

    DATABASE_PATH = os.getenv(
        "DATABASE_PATH",
        "data/cyber_shield.db"
    )