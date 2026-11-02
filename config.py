"""
Application Configuration Module
Handles environment variable loading, database parameters, and runtime settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(env_path)


class Config:
    """Base application configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "healthcare-dev-insecure-secret-key-2026")
    DEBUG = False
    TESTING = False

    # Database Engine: 'oracle' or 'sqlite'
    DB_ENGINE = os.getenv("DB_ENGINE", "sqlite").lower()

    # Oracle Database Free Settings
    ORACLE_USER = os.getenv("ORACLE_USER", "healthcare_admin")
    ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "")
    ORACLE_HOST = os.getenv("ORACLE_HOST", "localhost")
    ORACLE_PORT = int(os.getenv("ORACLE_PORT", "1521"))
    ORACLE_SERVICE_NAME = os.getenv("ORACLE_SERVICE_NAME", "FREEPDB1")
    ORACLE_CONNECT_TIMEOUT = int(os.getenv("ORACLE_CONNECT_TIMEOUT", "10"))

    # SQLite Database Settings (for testing/local development fallback)
    SQLITE_DB_PATH = os.getenv(
        "SQLITE_DB_PATH", str(BASE_DIR / "healthcare.db")
    )

    # Logging Settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", str(BASE_DIR / "logs" / "app.log"))

    # Pagination Defaults
    DEFAULT_PAGE = 1
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100

    @classmethod
    def get_oracle_dsn(cls) -> str:
        """Returns Easy Connect string for Oracle Database."""
        return f"{cls.ORACLE_HOST}:{cls.ORACLE_PORT}/{cls.ORACLE_SERVICE_NAME}"


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    DEBUG = True
    DB_ENGINE = "sqlite"
    SQLITE_DB_PATH = ":memory:"


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False
    DB_ENGINE = os.getenv("DB_ENGINE", "oracle").lower()


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config():
    """Retrieve configuration based on FLASK_ENV or DEFAULT."""
    env = os.getenv("FLASK_ENV", "development").lower()
    return config_by_name.get(env, DevelopmentConfig)
