"""
Integration Tests for Healthcare REST API Endpoints
Validates HTTP response codes, JSON payloads, headers, and routing layers.
"""

import json
import pytest


def test_health_check_endpoint(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"


def test_api_get_patients_paginated(client):
    res = client.get("/api/patients?page=1&page_size=10")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert len(data["data"]) == 10
    assert data["meta"]["total_records"] == 25


def test_api_register_patient_success(client):
    payload = {
        "first_name": "Clara",
        "last_name": "Barton",
        "date_of_birth": "1992-12-25",
        "gender": "Female",
        "blood_group": "O+",
        "email": "clara.barton@redcross.org",
        "phone": "555-7788",
        "address": "456 Red Cross Way",
    }
    res = client.post("/api/patients", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    assert data["data"]["first_name"] == "Clara"
    assert "patient_mrn" in data["data"]


def test_api_register_patient_validation_error(client):
    payload = {
        "first_name": "",  # Missing required
        "last_name": "Test",
    }
    res = client.post("/api/patients", json=payload)
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert "Patient validation failed" in data["error"]


def test_api_get_patient_by_id(client):
    res = client.get("/api/patients/1")
    assert res.status_code == 200
    data = res.get_json()
    assert data["data"]["patient_id"] == 1
    assert data["data"]["patient_mrn"] == "MRN-10001"


def test_api_get_patient_not_found(client):
    res = client.get("/api/patients/99999")
    assert res.status_code == 404
    data = res.get_json()
    assert data["success"] is False


def test_api_schedule_appointment_success(client):
    payload = {
        "patient_id": 1,
        "provider_id": 2,
        "appointment_date": "2026-12-20",
        "appointment_time": "11:00",
        "reason_for_visit": "Immunization Booster",
    }
    res = client.post("/api/appointments?allow_past=true", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["data"]["status"] == "SCHEDULED"


def test_api_schedule_appointment_conflict(client):
    # Provider 1 has appointment at 2026-11-15 09:00:00
    payload = {
        "patient_id": 2,
        "provider_id": 1,
        "appointment_date": "2026-11-15",
        "appointment_time": "09:00",
        "reason_for_visit": "Conflict visit",
    }
    res = client.post("/api/appointments?allow_past=true", json=payload)
    assert res.status_code == 409
    data = res.get_json()
    assert "conflict" in data["error"].lower()


def test_api_cancel_appointment(client):
    # Appointment 26 is SCHEDULED
    res = client.put("/api/appointments/26/cancel", json={"cancellation_reason": "Patient rescheduled"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["data"]["status"] == "CANCELLED"


def test_api_record_clinical_encounter(client):
    payload = {
        "patient_id": 1,
        "provider_id": 1,
        "encounter_type": "OUTPATIENT",
        "chief_complaint": "Arrhythmia check",
        "clinical_notes": "ECG stable. No medication change required.",
        "diagnosis_code": "I49.3",
        "diagnosis_description": "Ventricular premature depolarization",
        "billing_amount": 175.00,
    }
    res = client.post("/api/encounters", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["data"]["encounter_id"] is not None


def test_api_billing_payment(client):
    # Bill 4 has balance 200.00
    res = client.post("/api/billing/4/payment", json={
        "payment_amount": 50.00,
        "payment_method": "DEBIT_CARD",
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["data"]["balance_due"] == 150.00
    assert data["data"]["status"] == "PARTIALLY_PAID"


def test_api_report_monthly_billing(client):
    res = client.get("/api/reports/monthly-billing?year=2026")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0


def test_api_report_appointment_status(client):
    res = client.get("/api/reports/appointment-status")
    assert res.status_code == 200
    data = res.get_json()
    assert "department_breakdown" in data["data"]
    assert "status_distribution" in data["data"]


def test_api_report_provider_utilization(client):
    res = client.get("/api/reports/provider-utilization")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data["data"]) == 8  # 8 providers


def test_api_report_outstanding_billing(client):
    res = client.get("/api/reports/outstanding-billing")
    assert res.status_code == 200
    data = res.get_json()
    assert "aging_distribution" in data["data"]
    assert data["data"]["total_outstanding_amount"] > 0


def test_api_report_patient_visit_history(client):
    res = client.get("/api/reports/patient-visit-history/1")
    assert res.status_code == 200
    data = res.get_json()
    assert data["data"]["patient"]["patient_id"] == 1
    assert "timeline" in data["data"]


def test_api_dashboard_stats(client):
    res = client.get("/api/dashboard/stats")
    assert res.status_code == 200
    data = res.get_json()
    assert data["data"]["total_patients"] == 25
    assert data["data"]["total_providers"] == 8
    assert data["data"]["total_appointments"] == 29
