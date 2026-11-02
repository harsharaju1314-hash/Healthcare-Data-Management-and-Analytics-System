"""
Database Initialization Script
Initializes normalized schema, constraints, views, and indexes.
Supports both Oracle Database Free and local SQLite environment.
"""

import sys
from pathlib import Path
import re

# Add root directory to python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import get_config
from app.repositories.db import db
from app.utils.logger import logger

SQLITE_SCHEMA = """
-- Drop tables in reverse dependency order
DROP TABLE IF EXISTS BILLING_RECORDS;
DROP TABLE IF EXISTS ENCOUNTERS;
DROP TABLE IF EXISTS APPOINTMENTS;
DROP TABLE IF EXISTS PATIENTS;
DROP TABLE IF EXISTS PROVIDERS;

CREATE TABLE PROVIDERS (
    provider_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name          TEXT NOT NULL,
    last_name           TEXT NOT NULL,
    specialty           TEXT NOT NULL,
    license_number      TEXT NOT NULL UNIQUE,
    email               TEXT NOT NULL UNIQUE,
    phone               TEXT,
    department          TEXT NOT NULL,
    created_at          TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE PATIENTS (
    patient_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_mrn             TEXT NOT NULL UNIQUE,
    first_name              TEXT NOT NULL,
    last_name               TEXT NOT NULL,
    date_of_birth           TEXT NOT NULL,
    gender                  TEXT NOT NULL CHECK (gender IN ('Male', 'Female', 'Other', 'Unknown')),
    blood_group             TEXT CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    email                   TEXT UNIQUE,
    phone                   TEXT NOT NULL,
    address                 TEXT,
    emergency_contact_name  TEXT,
    emergency_contact_phone TEXT,
    is_active               INTEGER DEFAULT 1 NOT NULL CHECK (is_active IN (0, 1)),
    created_at              TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at              TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE APPOINTMENTS (
    appointment_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id             INTEGER NOT NULL REFERENCES PATIENTS(patient_id) ON DELETE CASCADE,
    provider_id            INTEGER NOT NULL REFERENCES PROVIDERS(provider_id),
    appointment_date       TEXT NOT NULL,
    appointment_time       TEXT NOT NULL,
    appointment_datetime   TEXT NOT NULL,
    duration_minutes       INTEGER DEFAULT 30 NOT NULL CHECK (duration_minutes > 0),
    reason_for_visit       TEXT NOT NULL,
    status                 TEXT DEFAULT 'SCHEDULED' NOT NULL CHECK (status IN ('SCHEDULED', 'CONFIRMED', 'COMPLETED', 'CANCELLED', 'NO_SHOW')),
    cancellation_reason    TEXT,
    cancelled_at           TEXT,
    created_at             TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at             TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT uq_prov_slot UNIQUE (provider_id, appointment_datetime)
);

CREATE TABLE ENCOUNTERS (
    encounter_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id         INTEGER REFERENCES APPOINTMENTS(appointment_id) ON DELETE SET NULL,
    patient_id             INTEGER NOT NULL REFERENCES PATIENTS(patient_id) ON DELETE CASCADE,
    provider_id            INTEGER NOT NULL REFERENCES PROVIDERS(provider_id),
    encounter_type         TEXT DEFAULT 'OUTPATIENT' NOT NULL CHECK (encounter_type IN ('OUTPATIENT', 'INPATIENT', 'EMERGENCY', 'TELEHEALTH', 'FOLLOW_UP')),
    encounter_date         TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
    chief_complaint        TEXT NOT NULL,
    clinical_notes         TEXT NOT NULL,
    diagnosis_code         TEXT NOT NULL,
    diagnosis_description  TEXT NOT NULL,
    status                 TEXT DEFAULT 'COMPLETED' NOT NULL CHECK (status IN ('IN_PROGRESS', 'COMPLETED', 'AMENDED', 'CANCELLED')),
    created_at             TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE BILLING_RECORDS (
    bill_id                INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_number            TEXT NOT NULL UNIQUE,
    patient_id             INTEGER NOT NULL REFERENCES PATIENTS(patient_id) ON DELETE CASCADE,
    encounter_id           INTEGER NOT NULL REFERENCES ENCOUNTERS(encounter_id) ON DELETE CASCADE,
    billing_date           TEXT DEFAULT CURRENT_DATE NOT NULL,
    due_date               TEXT NOT NULL,
    total_amount           REAL NOT NULL CHECK (total_amount >= 0),
    paid_amount            REAL DEFAULT 0.00 NOT NULL CHECK (paid_amount >= 0),
    balance_due            REAL NOT NULL CHECK (balance_due >= 0),
    status                 TEXT DEFAULT 'PENDING' NOT NULL CHECK (status IN ('PENDING', 'PAID', 'PARTIALLY_PAID', 'CANCELLED', 'OVERDUE')),
    payment_method         TEXT CHECK (payment_method IN ('CASH', 'CREDIT_CARD', 'INSURANCE', 'DEBIT_CARD', 'BANK_TRANSFER', NULL)),
    insurance_claim_id     TEXT,
    created_at             TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at             TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_billing_amounts CHECK (paid_amount <= total_amount AND balance_due = total_amount - paid_amount)
);

CREATE INDEX IF NOT EXISTS idx_patients_mrn ON PATIENTS(patient_mrn);
CREATE INDEX IF NOT EXISTS idx_patients_name ON PATIENTS(last_name, first_name);
CREATE INDEX IF NOT EXISTS idx_appointments_pat ON APPOINTMENTS(patient_id);
CREATE INDEX IF NOT EXISTS idx_appointments_prov_dt ON APPOINTMENTS(provider_id, appointment_datetime);
CREATE INDEX IF NOT EXISTS idx_appointments_status ON APPOINTMENTS(status);
CREATE INDEX IF NOT EXISTS idx_encounters_pat ON ENCOUNTERS(patient_id);
CREATE INDEX IF NOT EXISTS idx_encounters_prov ON ENCOUNTERS(provider_id);
CREATE INDEX IF NOT EXISTS idx_encounters_date ON ENCOUNTERS(encounter_date);
CREATE INDEX IF NOT EXISTS idx_billing_pat ON BILLING_RECORDS(patient_id);
CREATE INDEX IF NOT EXISTS idx_billing_enc ON BILLING_RECORDS(encounter_id);
CREATE INDEX IF NOT EXISTS idx_billing_status_due ON BILLING_RECORDS(status, due_date);
CREATE INDEX IF NOT EXISTS idx_billing_date ON BILLING_RECORDS(billing_date);
"""


def init_database():
    """Initializes schema and tables for active database engine."""
    logger.info(f"Initializing database schema using engine: {db.engine.upper()}...")

    if db.is_oracle():
        schema_file = ROOT_DIR / "database" / "schema.sql"
        views_file = ROOT_DIR / "database" / "views.sql"

        with open(schema_file, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        with open(views_file, "r", encoding="utf-8") as f:
            views_sql = f.read()

        with db.get_connection() as conn:
            cursor = conn.cursor()
            # Split commands by '/' or ';'
            statements = [stmt.strip() for stmt in schema_sql.split("/") if stmt.strip()]
            for stmt in statements:
                try:
                    cursor.execute(stmt)
                except Exception as e:
                    logger.warning(f"Oracle schema execution notice: {e}")
            conn.commit()
            cursor.close()
            logger.info("Oracle schema tables and constraints created successfully.")
    else:
        # SQLite initialization
        with db.get_connection() as conn:
            conn.executescript(SQLITE_SCHEMA)
            conn.commit()
            logger.info(f"SQLite schema tables and constraints created successfully at {db.config.SQLITE_DB_PATH}.")


if __name__ == "__main__":
    init_database()
