"""
Unit Tests for Request Payload Validators
"""

import pytest
from app.schemas.validators import (
    validate_patient_payload,
    validate_appointment_payload,
    validate_encounter_payload,
    validate_billing_payload,
    validate_payment_payload,
)
from app.utils.exceptions import ValidationException


def test_valid_patient_payload():
    payload = {
        "first_name": "Test",
        "last_name": "User",
        "date_of_birth": "1990-05-15",
        "gender": "Female",
        "blood_group": "O+",
        "email": "test.user@example.com",
        "phone": "555-0199",
    }
    validated = validate_patient_payload(payload)
    assert validated["first_name"] == "Test"


def test_patient_future_dob_fails():
    payload = {
        "first_name": "Future",
        "last_name": "Baby",
        "date_of_birth": "2099-01-01",
        "gender": "Male",
        "phone": "555-0199",
    }
    with pytest.raises(ValidationException) as exc:
        validate_patient_payload(payload)
    assert "date_of_birth cannot be a future date" in str(exc.value.details)


def test_patient_invalid_gender_fails():
    payload = {
        "first_name": "Invalid",
        "last_name": "Gender",
        "date_of_birth": "1995-01-01",
        "gender": "Nonexistent",
        "phone": "555-0199",
    }
    with pytest.raises(ValidationException) as exc:
        validate_patient_payload(payload)
    assert "gender must be one of" in str(exc.value.details)


def test_patient_invalid_email_fails():
    payload = {
        "first_name": "Bad",
        "last_name": "Email",
        "date_of_birth": "1995-01-01",
        "gender": "Male",
        "email": "not-an-email",
        "phone": "555-0199",
    }
    with pytest.raises(ValidationException) as exc:
        validate_patient_payload(payload)
    assert "Invalid email address format" in str(exc.value.details)


def test_appointment_validator_success():
    payload = {
        "patient_id": 1,
        "provider_id": 2,
        "appointment_date": "2026-12-01",
        "appointment_time": "14:30",
        "reason_for_visit": "Routine checkup",
        "duration_minutes": 30,
    }
    validated = validate_appointment_payload(payload)
    assert validated["appointment_time"] == "14:30"


def test_appointment_invalid_time_fails():
    payload = {
        "patient_id": 1,
        "provider_id": 2,
        "appointment_date": "2026-12-01",
        "appointment_time": "25:99",
        "reason_for_visit": "Routine checkup",
    }
    with pytest.raises(ValidationException) as exc:
        validate_appointment_payload(payload)
    assert "appointment_time must be in HH:MM format" in str(exc.value.details)


def test_encounter_validator_success():
    payload = {
        "patient_id": 1,
        "provider_id": 1,
        "encounter_type": "OUTPATIENT",
        "chief_complaint": "Persistent cough",
        "clinical_notes": "Chest clear. Prescribed rest.",
        "diagnosis_code": "J00",
        "diagnosis_description": "Acute nasopharyngitis",
        "billing_amount": 120.00,
    }
    validated = validate_encounter_payload(payload)
    assert validated["diagnosis_code"] == "J00"


def test_billing_negative_amount_fails():
    payload = {
        "patient_id": 1,
        "encounter_id": 1,
        "total_amount": -50.00,
    }
    with pytest.raises(ValidationException):
        validate_billing_payload(payload)


def test_payment_zero_amount_fails():
    payload = {
        "payment_amount": 0.00,
        "payment_method": "CREDIT_CARD",
    }
    with pytest.raises(ValidationException):
        validate_payment_payload(payload)
