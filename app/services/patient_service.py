"""
Patient Business Logic Service
Coordinates patient registration, validation, duplicate prevention, and profile management.
"""

from typing import Dict, Any, Tuple
from app.repositories.patient_repo import PatientRepository
from app.schemas.validators import validate_patient_payload
from app.utils.exceptions import ResourceNotFoundException, ConflictException
from app.utils.logger import logger


class PatientService:
    """Business logic service for patient management workflows."""

    @staticmethod
    def register_patient(data: Dict[str, Any]) -> Dict[str, Any]:
        """Registers a new patient with duplicate checks and input validation."""
        validated = validate_patient_payload(data, is_update=False)

        # Check duplicate email
        if validated.get("email"):
            existing = PatientRepository.get_by_email(validated["email"])
            if existing:
                raise ConflictException(f"Patient with email '{validated['email']}' already exists.")

        # Check duplicate MRN if manually provided
        if validated.get("patient_mrn"):
            existing_mrn = PatientRepository.get_by_mrn(validated["patient_mrn"])
            if existing_mrn:
                raise ConflictException(f"Patient with MRN '{validated['patient_mrn']}' already exists.")

        patient_id = PatientRepository.create(validated)
        logger.info(f"Successfully registered patient ID {patient_id}")
        return PatientRepository.get_by_id(patient_id)

    @staticmethod
    def get_patient(patient_id: int) -> Dict[str, Any]:
        """Retrieves patient details by ID or raises ResourceNotFoundException."""
        patient = PatientRepository.get_by_id(patient_id)
        if not patient:
            raise ResourceNotFoundException(f"Patient ID {patient_id} not found.")
        return patient

    @staticmethod
    def search_patients(query: str = None, page: int = 1, page_size: int = 20) -> Tuple[list, int]:
        """Searches patients with pagination."""
        offset = (page - 1) * page_size
        items = PatientRepository.search(query, limit=page_size, offset=offset)
        total = PatientRepository.count(query)
        return items, total

    @staticmethod
    def update_patient(patient_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates patient profile details."""
        PatientService.get_patient(patient_id)  # Validate existence
        validated = validate_patient_payload(data, is_update=True)

        if validated.get("email"):
            existing = PatientRepository.get_by_email(validated["email"])
            if existing and existing["patient_id"] != patient_id:
                raise ConflictException(f"Email '{validated['email']}' is already in use by another patient.")

        PatientRepository.update(patient_id, validated)
        return PatientRepository.get_by_id(patient_id)

    @staticmethod
    def deactivate_patient(patient_id: int) -> bool:
        """Deactivates a patient account."""
        PatientService.get_patient(patient_id)
        return PatientRepository.soft_delete(patient_id)
