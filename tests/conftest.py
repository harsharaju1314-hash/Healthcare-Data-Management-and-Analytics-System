"""
Pytest Fixtures and Test Environment Setup
Provides isolated in-memory test database and mock client fixtures.
"""

import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pytest
from config import TestingConfig
from app import create_app
from app.repositories.db import db
from scripts.init_db import SQLITE_SCHEMA
from scripts.seed_db import PROVIDERS_DATA, PATIENTS_DATA, APPOINTMENTS_DATA, ENCOUNTERS_DATA, BILLING_DATA


@pytest.fixture(scope="session")
def app():
    """Session-level application fixture configured for testing."""
    application = create_app(TestingConfig)
    return application


@pytest.fixture(scope="function")
def client(app):
    """Test client fixture with fresh database state per test function."""
    with app.test_client() as test_client:
        with app.app_context():
            # Setup isolated SQLite schema for test
            with db.get_connection() as conn:
                conn.executescript(SQLITE_SCHEMA)

                # Seed base deterministic data
                cursor = conn.cursor()
                prov_sql = """
                    INSERT INTO PROVIDERS (first_name, last_name, specialty, license_number, email, phone, department)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                for p in PROVIDERS_DATA:
                    cursor.execute(prov_sql, p)

                pat_sql = """
                    INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                for pt in PATIENTS_DATA:
                    cursor.execute(pat_sql, pt)

                appt_sql = """
                    INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status, cancellation_reason, cancelled_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                for ap in APPOINTMENTS_DATA:
                    cursor.execute(appt_sql, ap)

                enc_sql = """
                    INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                for en in ENCOUNTERS_DATA:
                    cursor.execute(enc_sql, en)

                bill_sql = """
                    INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                for bi in BILLING_DATA:
                    cursor.execute(bill_sql, bi)

                conn.commit()
                cursor.close()

            yield test_client
