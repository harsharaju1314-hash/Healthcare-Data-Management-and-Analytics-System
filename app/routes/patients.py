"""
Patient REST API Endpoints
"""

from flask import Blueprint, request
from app.services.patient_service import PatientService
from app.services.billing_service import BillingService
from app.utils.response import api_success, api_paginated
from app.utils.logger import logger

patients_bp = Blueprint("patients", __name__, url_prefix="/api/patients")


@patients_bp.route("", methods=["GET"])
def get_patients():
    """
    GET /api/patients
    Retrieves paginated list of patients with optional search query.
    """
    search_term = request.args.get("search", type=str)
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=20, type=int)

    items, total = PatientService.search_patients(search_term, page=page, page_size=page_size)
    return api_paginated(items, total=total, page=page, page_size=page_size, message="Patients retrieved successfully")


@patients_bp.route("", methods=["POST"])
def register_patient():
    """
    POST /api/patients
    Registers a new patient.
    """
    payload = request.get_json() or {}
    new_patient = PatientService.register_patient(payload)
    return api_success(data=new_patient, message="Patient registered successfully", status_code=201)


@patients_bp.route("/<int:patient_id>", methods=["GET"])
def get_patient(patient_id: int):
    """
    GET /api/patients/<patient_id>
    Retrieves a single patient record by ID.
    """
    patient = PatientService.get_patient(patient_id)
    return api_success(data=patient, message="Patient retrieved successfully")


@patients_bp.route("/<int:patient_id>", methods=["PUT"])
def update_patient(patient_id: int):
    """
    PUT /api/patients/<patient_id>
    Updates an existing patient's demographic or contact details.
    """
    payload = request.get_json() or {}
    updated = PatientService.update_patient(patient_id, payload)
    return api_success(data=updated, message="Patient updated successfully")


@patients_bp.route("/<int:patient_id>", methods=["DELETE"])
def deactivate_patient(patient_id: int):
    """
    DELETE /api/patients/<patient_id>
    Soft-deletes (deactivates) a patient record.
    """
    PatientService.deactivate_patient(patient_id)
    return api_success(message=f"Patient ID {patient_id} successfully deactivated")


@patients_bp.route("/<int:patient_id>/balance", methods=["GET"])
def get_patient_balance(patient_id: int):
    """
    GET /api/patients/<patient_id>/balance
    Calculates total unpaid balance for the patient.
    """
    balance_info = BillingService.get_patient_outstanding_balance(patient_id)
    return api_success(data=balance_info, message="Patient balance calculated successfully")
