"""
Database Diagnostics and Connectivity Test Script
Tests connectivity, verifies table row counts, and inspects database engine settings.
"""

import sys
from pathlib import Path

# Add root directory to python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import get_config
from app.repositories.db import db
from app.utils.logger import logger


def run_diagnostics():
    """Runs connectivity checks and prints summary diagnostic metrics."""
    config = get_config()

    print("=" * 65)
    print("HealthPulse Database Connectivity & Diagnostic Report")
    print("=" * 65)
    print(f"Configured Engine      : {config.DB_ENGINE.upper()}")
    print(f"Active Connected Engine: {db.engine.upper()}")
    print(f"Is Oracle Native       : {db.is_oracle()}")

    if db.is_oracle():
        print(f"Oracle Host            : {config.ORACLE_HOST}:{config.ORACLE_PORT}")
        print(f"Oracle Service Name    : {config.ORACLE_SERVICE_NAME}")
        print(f"Oracle User            : {config.ORACLE_USER}")
    else:
        print(f"SQLite Database Path   : {config.SQLITE_DB_PATH}")

    print("-" * 65)

    # Ping database
    try:
        ping = db.execute_one("SELECT 1 AS status")
        print(f"Database Ping          : SUCCESS (Result: {ping.get('status')})")
    except Exception as e:
        print(f"Database Ping          : FAILED ({e})")
        return

    # Count table records
    tables = ["PROVIDERS", "PATIENTS", "APPOINTMENTS", "ENCOUNTERS", "BILLING_RECORDS"]
    print("\nTable Record Counts:")
    for t in tables:
        try:
            res = db.execute_one(f"SELECT COUNT(*) AS total FROM {t}")
            cnt = res.get("total", 0) if res else 0
            print(f"  - {t:<20}: {cnt:>5} records")
        except Exception as e:
            print(f"  - {t:<20}: ERROR ({e})")

    print("=" * 65)


if __name__ == "__main__":
    run_diagnostics()
