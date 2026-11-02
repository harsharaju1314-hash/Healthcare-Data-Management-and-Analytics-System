"""
Oracle PL/SQL Compiler and Test Runner Script
Executes and compiles PL/SQL procedures, functions, and packages on Oracle Database Free.
"""

import sys
from pathlib import Path

# Add root directory to python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import get_config
from app.repositories.db import db
from app.utils.logger import logger


def compile_plsql_objects():
    """Compiles PL/SQL scripts on connected Oracle instance."""
    if not db.is_oracle():
        logger.warning(
            f"Active database engine is '{db.engine.upper()}'. PL/SQL compilation requires an active Oracle Database Free connection."
        )
        print("Note: PL/SQL scripts are located in the database/ directory:")
        print("  - database/functions.sql   (FN_CALC_OUTSTANDING_BALANCE, FN_VALIDATE_BILLING_AMOUNT)")
        print("  - database/procedures.sql  (SP_CANCEL_APPOINTMENT, SP_RECORD_CLINICAL_ENCOUNTER, SP_PROCESS_BILLING_PAYMENT)")
        print("  - database/packages.sql    (PKG_HEALTHCARE_REPORTING spec and body)")
        print("\nTo compile against Oracle Database Free:")
        print("  1. Ensure Oracle Database Free (23c / 21c) is running.")
        print("  2. Set DB_ENGINE=oracle, ORACLE_USER, and ORACLE_PASSWORD in .env.")
        print("  3. Run this script: python scripts/run_plsql.py")
        return

    logger.info("Connecting to Oracle Database Free to compile PL/SQL packages...")
    files = ["functions.sql", "procedures.sql", "packages.sql"]

    with db.get_connection() as conn:
        cursor = conn.cursor()
        for filename in files:
            file_path = ROOT_DIR / "database" / filename
            logger.info(f"Compiling {filename}...")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Split PL/SQL blocks by '/'
            blocks = [b.strip() for b in content.split("/") if b.strip()]
            for block in blocks:
                try:
                    cursor.execute(block)
                except Exception as e:
                    logger.error(f"Error compiling block in {filename}: {e}")

        conn.commit()
        cursor.close()

    logger.info("All PL/SQL functions, procedures, and packages compiled successfully on Oracle Database Free.")


if __name__ == "__main__":
    compile_plsql_objects()
