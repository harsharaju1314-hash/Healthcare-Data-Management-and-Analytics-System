"""
Unit Tests for Appointment Service Workflows
"""

import pytest
from app.services.appointment_service import AppointmentService
from app.utils.exceptions import ConflictException, ValidationException, ResourceNotFoundException


def test_schedule_appointment_success(client):
    payload = {
        "patient_id": 1,
        "provider_id": 1,
        "appointment_date": "2026-12-15",
        "appointment_time": "10:00",
        "reason_for_visit": "Follow up consultation",
        "duration_minutes": 30,
    }
    appt = AppointmentService.schedule_appointment(payload)
    assert appt["appointment_id"] is not None
    assert appt["status"] == "SCHEDULED"


def test_schedule_appointment_past_date_fails(client):
    payload = {
        "patient_id": 1,
        "provider_id": 1,
        "appointment_date": "2020-01-01",
        "appointment_time": "10:00",
        "reason_for_visit": "Old consultation",
    }
    with pytest.raises(ValidationException) as exc:
        AppointmentService.schedule_appointment(payload, allow_past=False)
    assert "cannot be scheduled in the past" in str(exc.value)


def test_schedule_conflicting_appointment_fails(client):
    # Provider 1 has appointment at 2026-11-15 09:00:00 in seed data
    payload = {
        "patient_id": 2,
        "provider_id": 1,
        "appointment_date": "2026-11-15",
        "appointment_time": "09:00",
        "reason_for_visit": "Overlapping slot",
    }
    with pytest.raises(ConflictException) as exc:
        AppointmentService.schedule_appointment(payload, allow_past=True)
    assert "Scheduling conflict" in str(exc.value)


def test_cancel_appointment_success(client):
    # Appointment 26 is SCHEDULED in seed data
    cancelled = AppointmentService.cancel_appointment(26, reason="Patient requested cancellation")
    assert cancelled["status"] == "CANCELLED"
    assert cancelled["cancellation_reason"] == "Patient requested cancellation"


def test_cancel_completed_appointment_fails(client):
    # Appointment 1 is COMPLETED in seed data
    with pytest.raises(ConflictException) as exc:
        AppointmentService.cancel_appointment(1, reason="Cannot cancel finished visit")
    assert "already been completed" in str(exc.value)


def test_cancel_already_cancelled_appointment_fails(client):
    # Appointment 4 is CANCELLED in seed data
    with pytest.raises(ConflictException) as exc:
        AppointmentService.cancel_appointment(4, reason="Trying again")
    assert "already cancelled" in str(exc.value)
