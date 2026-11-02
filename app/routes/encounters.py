"""
Clinical Encounter REST API Endpoints
"""

from flask import Blueprint, request
from app.services.encounter_service import EncounterService
from app.utils.response import api_success, api_paginated

encounters_bp = Blueprint("encounters", __name__, url_prefix="/api/encounters")


@encounters_bp.route("", methods=["GET"])
def get_encounters():
    """
    GET /api/encounters
    Retrieves paginated list of clinical encounters.
    """
    patient_id = request.args.get("patient_id", type=int)
    provider_id = request.args.get("provider_id", type=int)
    encounter_type = request.args.get("encounter_type", type=str)
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=20, type=int)

    items, total = EncounterService.list_encounters(
        patient_id=patient_id,
        provider_id=provider_id,
        encounter_type=encounter_type,
        page=page,
        page_size=page_size,
    )
    return api_paginated(items, total=total, page=page, page_size=page_size, message="Encounters retrieved successfully")


@encounters_bp.route("", methods=["POST"])
def record_encounter():
    """
    POST /api/encounters
    Records a clinical encounter and optionally creates an associated invoice.
    """
    payload = request.get_json() or {}
    new_enc = EncounterService.record_encounter(payload)
    return api_success(data=new_enc, message="Clinical encounter recorded successfully", status_code=201)


@encounters_bp.route("/<int:encounter_id>", methods=["GET"])
def get_encounter(encounter_id: int):
    """
    GET /api/encounters/<encounter_id>
    Retrieves detailed clinical encounter by ID.
    """
    enc = EncounterService.get_encounter(encounter_id)
    return api_success(data=enc, message="Encounter retrieved successfully")
