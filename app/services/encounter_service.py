"""
Clinical Encounter Business Logic Service
Simulates the core clinical documentation workflow: intake, consultation, diagnosis,
appointment completion, and automatic charge generation.
"""

from typing import Dict, Any, Tuple, Optional
from app.repositories.encounter_repo import EncounterRepository
from app.repositories.patient_repo import PatientRepository
from app.repositories.provider_repo import ProviderRepository
from app.repositories.appointment_repo import AppointmentRepository
from app.repositories.billing_repo import BillingRepository
from app.schemas.validators import validate_encounter_payload
from app.utils.exceptions import ResourceNotFoundException, ValidationException
from app.utils.decimal_utils import to_decimal
from app.utils.logger import logger


class EncounterService:
    """Business logic service for clinical encounter workflows."""

    @staticmethod
    def record_encounter(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the clinical encounter workflow:
        1. Validates patient, provider, and encounter data.
        2. If linked to an appointment, validates match and updates appointment to COMPLETED.
        3. Inserts encounter record.
        4. If billing amount provided, automatically generates initial billing record.
        """
        validated = validate_encounter_payload(data)

        patient_id = validated["patient_id"]
        provider_id = validated["provider_id"]
        appt_id = validated.get("appointment_id")

        # Validate patient
        patient = PatientRepository.get_by_id(patient_id)
        if not patient:
            raise ResourceNotFoundException(f"Patient ID {patient_id} not found.")

        # Validate provider
        provider = ProviderRepository.get_by_id(provider_id)
        if not provider:
            raise ResourceNotFoundException(f"Provider ID {provider_id} not found.")

        # Validate appointment if linked
        if appt_id:
            appt = AppointmentRepository.get_by_id(appt_id)
            if not appt:
                raise ResourceNotFoundException(f"Linked appointment ID {appt_id} not found.")
            if appt["patient_id"] != patient_id:
                raise ValidationException("Appointment patient does not match encounter patient.")
            if appt["provider_id"] != provider_id:
                raise ValidationException("Appointment provider does not match encounter provider.")

        # Insert encounter
        encounter_id = EncounterRepository.create(validated)
        logger.info(f"Recorded clinical encounter ID {encounter_id} for Patient {patient_id}")

        # Update appointment status to COMPLETED if linked
        if appt_id:
            AppointmentRepository.update_status(appt_id, "COMPLETED")

        # Auto-generate bill if amount specified
        billing_amount = validated.get("billing_amount")
        bill_id = None
        if billing_amount is not None and to_decimal(billing_amount) > 0:
            bill_data = {
                "patient_id": patient_id,
                "encounter_id": encounter_id,
                "total_amount": billing_amount,
            }
            bill_id = BillingRepository.create(bill_data)
            logger.info(f"Generated invoice ID {bill_id} for Encounter {encounter_id}")

        encounter = EncounterRepository.get_by_id(encounter_id)
        return encounter

    @staticmethod
    def get_encounter(encounter_id: int) -> Dict[str, Any]:
        """Retrieves clinical encounter details or raises 404."""
        enc = EncounterRepository.get_by_id(encounter_id)
        if not enc:
            raise ResourceNotFoundException(f"Encounter ID {encounter_id} not found.")
        return enc

    @staticmethod
    def list_encounters(patient_id: Optional[int] = None,
                        provider_id: Optional[int] = None,
                        encounter_type: Optional[str] = None,
                        page: int = 1,
                        page_size: int = 20) -> Tuple[list, int]:
        """Lists encounters with filtering and pagination."""
        offset = (page - 1) * page_size
        items = EncounterRepository.get_list(
            patient_id=patient_id,
            provider_id=provider_id,
            encounter_type=encounter_type,
            limit=page_size,
            offset=offset,
        )
        total = EncounterRepository.count(
            patient_id=patient_id,
            provider_id=provider_id,
            encounter_type=encounter_type,
        )
        return items, total
