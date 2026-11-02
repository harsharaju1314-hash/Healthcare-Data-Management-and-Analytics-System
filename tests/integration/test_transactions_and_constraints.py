"""
Integration Tests for Database Transactions and Schema Constraints
Validates transactional rollback and database constraint enforcement.
"""

import pytest
from app.repositories.db import db
from app.utils.exceptions import ConflictException, DatabaseException


def test_transaction_rollback_on_failure(client):
    """
    Verifies that when a batch of SQL operations fails mid-way,
    the entire transaction is rolled back and no partial records persist.
    """
    initial_patients = db.execute_one("SELECT COUNT(*) as cnt FROM PATIENTS")["cnt"]

    # Attempt transaction where 1st statement is valid, but 2nd statement fails (invalid gender check constraint)
    statements = [
        (
            """
            INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, phone)
            VALUES ('MRN-ROLLBACK-1', 'Valid', 'User', '1990-01-01', 'Male', '555-0011')
            """,
            {}
        ),
        (
            """
            INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, phone)
            VALUES ('MRN-ROLLBACK-2', 'Invalid', 'User', '1990-01-01', 'IllegalGender', '555-0022')
            """,
            {}
        ),
    ]

    with pytest.raises((ConflictException, DatabaseException)):
        db.execute_transaction(statements)

    # Confirm that neither record was committed (atomic rollback)
    final_patients = db.execute_one("SELECT COUNT(*) as cnt FROM PATIENTS")["cnt"]
    assert final_patients == initial_patients

    # Ensure MRN-ROLLBACK-1 does not exist
    orphan = db.execute_one("SELECT * FROM PATIENTS WHERE patient_mrn = 'MRN-ROLLBACK-1'")
    assert orphan is None


def test_unique_mrn_constraint_enforced(client):
    """Verifies that inserting a duplicate MRN raises a ConflictException."""
    sql = """
        INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, phone)
        VALUES ('MRN-10001', 'Duplicate', 'MRN', '1990-01-01', 'Male', '555-9999')
    """
    with pytest.raises(ConflictException):
        db.execute_non_query(sql)


def test_unique_provider_license_enforced(client):
    """Verifies duplicate provider medical license is rejected."""
    sql = """
        INSERT INTO PROVIDERS (first_name, last_name, specialty, license_number, email, phone, department)
        VALUES ('Duplicate', 'Doc', 'Cardiology', 'MD-CARD-101', 'newdoc@hospital.org', '555-9999', 'Cardiovascular')
    """
    with pytest.raises(ConflictException):
        db.execute_non_query(sql)


def test_billing_negative_amount_constraint_enforced(client):
    """Verifies that negative billing amounts violate CHECK constraints."""
    sql = """
        INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status)
        VALUES ('INV-TEST-NEG', 1, 1, '2026-05-01', '2026-06-01', -100.00, 0.00, -100.00, 'PENDING')
    """
    with pytest.raises(ConflictException):
        db.execute_non_query(sql)


def test_billing_paid_exceeds_total_constraint_enforced(client):
    """Verifies CHECK constraint: paid_amount <= total_amount AND balance_due = total - paid."""
    sql = """
        INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status)
        VALUES ('INV-TEST-MATH', 1, 1, '2026-05-01', '2026-06-01', 100.00, 150.00, -50.00, 'PENDING')
    """
    with pytest.raises(ConflictException):
        db.execute_non_query(sql)
