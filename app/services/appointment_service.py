"""
Appointment Business Logic Service
Coordinates appointment scheduling, conflict detection, cancellation workflows, and status tracking.
"""

from typing import Dict, Any, Tuple, Optional
from datetime import datetime, date
from app.repositories.appointment_repo import AppointmentRepository
from app.repositories.patient_repo import PatientRepository
from app.repositories.provider_repo import ProviderRepository
from app.schemas.validators import validate_appointment_payload
from app.utils.exceptions import ResourceNotFoundException, ConflictException, ValidationException
from app.utils.logger import logger


class AppointmentService:
    """Business logic service for appointment management workflows."""

    @staticmethod
    def schedule_appointment(data: Dict[str, Any], allow_past: bool = False) -> Dict[str, Any]:
        """
        Schedules a new appointment with provider conflict checks and patient/provider validation.
        """
        validated = validate_appointment_payload(data)

        patient_id = validated["patient_id"]
        provider_id = validated["provider_id"]
        appt_date_str = validated["appointment_date"]
        appt_time_str = validated["appointment_time"]

        # Validate patient exists and is active
        patient = PatientRepository.get_by_id(patient_id)
        if not patient:
            raise ResourceNotFoundException(f"Patient ID {patient_id} not found.")
        if not patient.get("is_active", 1):
            raise ValidationException(f"Cannot schedule appointment for deactivated patient ID {patient_id}.")

        # Validate provider exists
        provider = ProviderRepository.get_by_id(provider_id)
        if not provider:
            raise ResourceNotFoundException(f"Provider ID {provider_id} not found.")

        # Check date not in the past (unless past dates explicitly permitted for historical records)
        if not allow_past:
            appt_date = datetime.strptime(appt_date_str, "%Y-%m-%d").date()
            if appt_date < date.today():
                raise ValidationException("Appointment date cannot be scheduled in the past.")

        # Check for provider time-slot conflict
        appt_datetime_str = f"{appt_date_str} {appt_time_str}:00"
        if AppointmentRepository.check_conflict(provider_id, appt_datetime_str):
            raise ConflictException(
                f"Scheduling conflict: Dr. {provider['last_name']} already has an active appointment at {appt_datetime_str}."
            )

        appointment_id = AppointmentRepository.create(validated)
        logger.info(f"Scheduled appointment ID {appointment_id} for Patient {patient_id} with Provider {provider_id}")
        return AppointmentRepository.get_by_id(appointment_id)

    @staticmethod
    def cancel_appointment(appointment_id: int, reason: str) -> Dict[str, Any]:
        """
        Safely cancels an appointment with state validation and mandatory cancellation reason.
        """
        if not reason or not reason.strip():
            raise ValidationException("A valid cancellation reason is required.")

        appt = AppointmentRepository.get_by_id(appointment_id)
        if not appt:
            raise ResourceNotFoundException(f"Appointment ID {appointment_id} not found.")

        current_status = appt.get("status")
        if current_status == "CANCELLED":
            raise ConflictException("Appointment is already cancelled.")
        if current_status == "COMPLETED":
            raise ConflictException("Cannot cancel an appointment that has already been completed.")

        AppointmentRepository.cancel(appointment_id, reason.strip())
        logger.info(f"Cancelled appointment ID {appointment_id}. Reason: {reason.strip()}")
        return AppointmentRepository.get_by_id(appointment_id)

    @staticmethod
    def get_appointment(appointment_id: int) -> Dict[str, Any]:
        """Retrieves appointment details or raises 404."""
        appt = AppointmentRepository.get_by_id(appointment_id)
        if not appt:
            raise ResourceNotFoundException(f"Appointment ID {appointment_id} not found.")
        return appt

    @staticmethod
    def list_appointments(patient_id: Optional[int] = None,
                          provider_id: Optional[int] = None,
                          status: Optional[str] = None,
                          start_date: Optional[str] = None,
                          end_date: Optional[str] = None,
                          page: int = 1,
                          page_size: int = 20) -> Tuple[list, int]:
        """Lists appointments with filtering and pagination."""
        offset = (page - 1) * page_size
        items = AppointmentRepository.get_list(
            patient_id=patient_id,
            provider_id=provider_id,
            status=status,
            start_date=start_date,
            end_date=end_date,
            limit=page_size,
            offset=offset,
        )
        total = AppointmentRepository.count(
            patient_id=patient_id,
            provider_id=provider_id,
            status=status,
            start_date=start_date,
            end_date=end_date,
        )
        return items, total
