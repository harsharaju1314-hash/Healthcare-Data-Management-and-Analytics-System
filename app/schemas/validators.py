"""
Request Payloads Validation Module
Performs comprehensive validation on incoming data payloads before hitting services/repositories.
"""

import re
from datetime import datetime, date
from decimal import Decimal
from typing import Dict, Any, List
from app.utils.exceptions import ValidationException
from app.utils.decimal_utils import to_decimal

EMAIL_REGEX = re.compile(r"^[\w\.\+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-\.]+$")
TIME_REGEX = re.compile(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")
VALID_GENDERS = {"Male", "Female", "Other", "Unknown"}
VALID_BLOOD_GROUPS = {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}
VALID_ENCOUNTER_TYPES = {"OUTPATIENT", "INPATIENT", "EMERGENCY", "TELEHEALTH", "FOLLOW_UP"}
VALID_ENCOUNTER_STATUSES = {"IN_PROGRESS", "COMPLETED", "AMENDED", "CANCELLED"}
VALID_APPOINTMENT_STATUSES = {"SCHEDULED", "CONFIRMED", "COMPLETED", "CANCELLED", "NO_SHOW"}
VALID_BILLING_STATUSES = {"PENDING", "PAID", "PARTIALLY_PAID", "CANCELLED", "OVERDUE"}
VALID_PAYMENT_METHODS = {"CASH", "CREDIT_CARD", "INSURANCE", "DEBIT_CARD", "BANK_TRANSFER"}


def validate_patient_payload(data: Dict[str, Any], is_update: bool = False) -> Dict[str, Any]:
    """Validates patient registration and update payloads."""
    errors: List[str] = []

    if not is_update or "first_name" in data:
        fn = str(data.get("first_name", "")).strip()
        if not fn or len(fn) > 50:
            errors.append("first_name is required and must be 1 to 50 characters.")

    if not is_update or "last_name" in data:
        ln = str(data.get("last_name", "")).strip()
        if not ln or len(ln) > 50:
            errors.append("last_name is required and must be 1 to 50 characters.")

    if not is_update or "date_of_birth" in data:
        dob_str = str(data.get("date_of_birth", "")).strip()
        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            if dob > date.today():
                errors.append("date_of_birth cannot be a future date.")
        except (ValueError, TypeError):
            errors.append("date_of_birth must be a valid date in YYYY-MM-DD format.")

    if not is_update or "gender" in data:
        gender = str(data.get("gender", "")).strip()
        if gender not in VALID_GENDERS:
            errors.append(f"gender must be one of: {', '.join(sorted(VALID_GENDERS))}")

    if data.get("blood_group"):
        bg = str(data.get("blood_group")).strip()
        if bg not in VALID_BLOOD_GROUPS:
            errors.append(f"blood_group must be one of: {', '.join(sorted(VALID_BLOOD_GROUPS))}")

    if data.get("email"):
        email = str(data.get("email")).strip()
        if not EMAIL_REGEX.match(email):
            errors.append("Invalid email address format.")

    if not is_update or "phone" in data:
        phone = str(data.get("phone", "")).strip()
        if not phone or len(phone) < 7 or len(phone) > 20:
            errors.append("phone is required and must be between 7 and 20 characters.")

    if errors:
        raise ValidationException(message="Patient validation failed", details={"errors": errors})

    return data


def validate_appointment_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validates appointment scheduling payloads."""
    errors: List[str] = []

    try:
        patient_id = int(data.get("patient_id", 0))
        if patient_id <= 0:
            errors.append("patient_id must be a positive integer.")
    except (ValueError, TypeError):
        errors.append("patient_id is required and must be a valid integer.")

    try:
        provider_id = int(data.get("provider_id", 0))
        if provider_id <= 0:
            errors.append("provider_id must be a positive integer.")
    except (ValueError, TypeError):
        errors.append("provider_id is required and must be a valid integer.")

    date_str = str(data.get("appointment_date", "")).strip()
    try:
        appt_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        errors.append("appointment_date must be a valid date in YYYY-MM-DD format.")
        appt_date = None

    time_str = str(data.get("appointment_time", "")).strip()
    if not TIME_REGEX.match(time_str):
        errors.append("appointment_time must be in HH:MM format (24-hour clock, e.g. 09:30).")

    reason = str(data.get("reason_for_visit", "")).strip()
    if not reason or len(reason) > 255:
        errors.append("reason_for_visit is required (1 to 255 characters).")

    duration = data.get("duration_minutes", 30)
    try:
        dur = int(duration)
        if dur <= 0 or dur > 240:
            errors.append("duration_minutes must be between 1 and 240.")
    except (ValueError, TypeError):
        errors.append("duration_minutes must be an integer.")

    if errors:
        raise ValidationException(message="Appointment validation failed", details={"errors": errors})

    return data


def validate_encounter_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validates clinical encounter creation payloads."""
    errors: List[str] = []

    try:
        patient_id = int(data.get("patient_id", 0))
        if patient_id <= 0:
            errors.append("patient_id must be a positive integer.")
    except (ValueError, TypeError):
        errors.append("patient_id must be a valid positive integer.")

    try:
        provider_id = int(data.get("provider_id", 0))
        if provider_id <= 0:
            errors.append("provider_id must be a positive integer.")
    except (ValueError, TypeError):
        errors.append("provider_id must be a valid positive integer.")

    enc_type = str(data.get("encounter_type", "OUTPATIENT")).strip()
    if enc_type not in VALID_ENCOUNTER_TYPES:
        errors.append(f"encounter_type must be one of: {', '.join(sorted(VALID_ENCOUNTER_TYPES))}")

    complaint = str(data.get("chief_complaint", "")).strip()
    if not complaint or len(complaint) > 500:
        errors.append("chief_complaint is required (1 to 500 characters).")

    notes = str(data.get("clinical_notes", "")).strip()
    if not notes:
        errors.append("clinical_notes is required.")

    code = str(data.get("diagnosis_code", "")).strip()
    if not code or len(code) > 20:
        errors.append("diagnosis_code is required (e.g. ICD-10 code, 1 to 20 characters).")

    desc = str(data.get("diagnosis_description", "")).strip()
    if not desc or len(desc) > 255:
        errors.append("diagnosis_description is required (1 to 255 characters).")

    if data.get("billing_amount") is not None:
        try:
            amt = to_decimal(data.get("billing_amount"))
            if amt < Decimal("0.00"):
                errors.append("billing_amount cannot be negative.")
        except Exception:
            errors.append("billing_amount must be a valid non-negative number.")

    if errors:
        raise ValidationException(message="Encounter validation failed", details={"errors": errors})

    return data


def validate_billing_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validates billing invoice generation payloads."""
    errors: List[str] = []

    try:
        patient_id = int(data.get("patient_id", 0))
        if patient_id <= 0:
            errors.append("patient_id must be a positive integer.")
    except (ValueError, TypeError):
        errors.append("patient_id is required.")

    try:
        encounter_id = int(data.get("encounter_id", 0))
        if encounter_id <= 0:
            errors.append("encounter_id must be a positive integer.")
    except (ValueError, TypeError):
        errors.append("encounter_id is required.")

    try:
        total = to_decimal(data.get("total_amount"))
        if total <= Decimal("0.00"):
            errors.append("total_amount must be greater than zero.")
    except Exception:
        errors.append("total_amount must be a valid positive number.")

    if data.get("due_date"):
        try:
            datetime.strptime(str(data["due_date"]).strip(), "%Y-%m-%d")
        except ValueError:
            errors.append("due_date must be in YYYY-MM-DD format.")

    if errors:
        raise ValidationException(message="Billing validation failed", details={"errors": errors})

    return data


def validate_payment_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validates payment application payloads."""
    errors: List[str] = []

    try:
        amt = to_decimal(data.get("payment_amount"))
        if amt <= Decimal("0.00"):
            errors.append("payment_amount must be greater than zero.")
    except Exception:
        errors.append("payment_amount must be a valid positive number.")

    method = data.get("payment_method")
    if method and method not in VALID_PAYMENT_METHODS:
        errors.append(f"payment_method must be one of: {', '.join(sorted(VALID_PAYMENT_METHODS))}")

    if errors:
        raise ValidationException(message="Payment validation failed", details={"errors": errors})

    return data
