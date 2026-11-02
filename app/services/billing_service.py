"""
Billing Business Logic Service
Coordinates invoice creation, exact decimal payment processing, balance tracking, and financial reconciliation.
"""

from typing import Dict, Any, Tuple, Optional
from decimal import Decimal
from app.repositories.billing_repo import BillingRepository
from app.repositories.patient_repo import PatientRepository
from app.repositories.encounter_repo import EncounterRepository
from app.schemas.validators import validate_billing_payload, validate_payment_payload
from app.utils.exceptions import ResourceNotFoundException, ConflictException, ValidationException
from app.utils.decimal_utils import to_decimal
from app.utils.logger import logger


class BillingService:
    """Business logic service for billing and revenue management."""

    @staticmethod
    def create_bill(data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a billing invoice for an encounter."""
        validated = validate_billing_payload(data)

        patient_id = validated["patient_id"]
        encounter_id = validated["encounter_id"]

        patient = PatientRepository.get_by_id(patient_id)
        if not patient:
            raise ResourceNotFoundException(f"Patient ID {patient_id} not found.")

        encounter = EncounterRepository.get_by_id(encounter_id)
        if not encounter:
            raise ResourceNotFoundException(f"Encounter ID {encounter_id} not found.")

        # Check if encounter already has an invoice
        existing_bill = BillingRepository.get_by_encounter_id(encounter_id)
        if existing_bill:
            raise ConflictException(f"Invoice already exists for Encounter ID {encounter_id} (Bill: {existing_bill['bill_number']}).")

        bill_id = BillingRepository.create(validated)
        logger.info(f"Created bill ID {bill_id} for Patient {patient_id}")
        return BillingRepository.get_by_id(bill_id)

    @staticmethod
    def process_payment(bill_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processes payment for an existing invoice."""
        validated = validate_payment_payload(data)
        payment_amount = to_decimal(validated["payment_amount"])
        payment_method = validated.get("payment_method", "CREDIT_CARD")

        result = BillingRepository.apply_payment(bill_id, payment_amount, payment_method)
        logger.info(f"Applied payment of ${payment_amount} to Bill ID {bill_id}. New status: {result['status']}")
        return result

    @staticmethod
    def get_bill(bill_id: int) -> Dict[str, Any]:
        """Retrieves an invoice by ID or raises 404."""
        bill = BillingRepository.get_by_id(bill_id)
        if not bill:
            raise ResourceNotFoundException(f"Invoice ID {bill_id} not found.")
        return bill

    @staticmethod
    def list_bills(patient_id: Optional[int] = None,
                   status: Optional[str] = None,
                   page: int = 1,
                   page_size: int = 20) -> Tuple[list, int]:
        """Lists invoices with filtering and pagination."""
        offset = (page - 1) * page_size
        items = BillingRepository.get_list(
            patient_id=patient_id,
            status=status,
            limit=page_size,
            offset=offset,
        )
        total = BillingRepository.count(patient_id=patient_id, status=status)
        return items, total

    @staticmethod
    def get_patient_outstanding_balance(patient_id: int) -> Dict[str, Any]:
        """Calculates total outstanding balance for a given patient."""
        patient = PatientRepository.get_by_id(patient_id)
        if not patient:
            raise ResourceNotFoundException(f"Patient ID {patient_id} not found.")

        balance = BillingRepository.get_patient_balance(patient_id)
        return {
            "patient_id": patient_id,
            "patient_mrn": patient["patient_mrn"],
            "patient_name": f"{patient['first_name']} {patient['last_name']}",
            "outstanding_balance": float(balance),
        }
