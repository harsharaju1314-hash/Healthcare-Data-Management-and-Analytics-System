"""
Unit Tests for Patient Service Workflows
"""

import pytest
from app.services.patient_service import PatientService
from app.utils.exceptions import ResourceNotFoundException, ConflictException


def test_register_patient_service_success(client):
    payload = {
        "first_name": "Marcus",
        "last_name": "Aurelius",
        "date_of_birth": "1980-04-26",
        "gender": "Male",
        "blood_group": "AB+",
        "email": "marcus.aurelius@rome.org",
        "phone": "555-4433",
    }
    patient = PatientService.register_patient(payload)
    assert patient["patient_id"] is not None
    assert patient["first_name"] == "Marcus"
    assert patient["patient_mrn"].startswith("MRN-")


def test_register_patient_duplicate_email(client):
    payload = {
        "first_name": "Duplicate",
        "last_name": "User",
        "date_of_birth": "1990-01-01",
        "gender": "Male",
        "email": "john.doe@fakeemail.com",  # Exists in seed data
        "phone": "555-9988",
    }
    with pytest.raises(ConflictException) as exc:
        PatientService.register_patient(payload)
    assert "already exists" in str(exc.value)


def test_get_nonexistent_patient_raises_404(client):
    with pytest.raises(ResourceNotFoundException):
        PatientService.get_patient(99999)


def test_update_patient_service(client):
    updated = PatientService.update_patient(1, {"phone": "555-8888"})
    assert updated["phone"] == "555-8888"


def test_deactivate_patient_service(client):
    success = PatientService.deactivate_patient(1)
    assert success is True
    p = PatientService.get_patient(1)
    assert p["is_active"] == 0
