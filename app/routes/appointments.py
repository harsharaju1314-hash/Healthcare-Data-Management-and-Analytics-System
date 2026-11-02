"""
Appointment REST API Endpoints
"""

from flask import Blueprint, request
from app.services.appointment_service import AppointmentService
from app.utils.response import api_success, api_paginated

appointments_bp = Blueprint("appointments", __name__, url_prefix="/api/appointments")


@appointments_bp.route("", methods=["GET"])
def get_appointments():
    """
    GET /api/appointments
    Retrieves filtered appointments with pagination.
    """
    patient_id = request.args.get("patient_id", type=int)
    provider_id = request.args.get("provider_id", type=int)
    status = request.args.get("status", type=str)
    start_date = request.args.get("start_date", type=str)
    end_date = request.args.get("end_date", type=str)
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=20, type=int)

    items, total = AppointmentService.list_appointments(
        patient_id=patient_id,
        provider_id=provider_id,
        status=status,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size,
    )
    return api_paginated(items, total=total, page=page, page_size=page_size, message="Appointments retrieved successfully")


@appointments_bp.route("", methods=["POST"])
def schedule_appointment():
    """
    POST /api/appointments
    Schedules a new appointment with conflict detection.
    """
    payload = request.get_json() or {}
    allow_past = request.args.get("allow_past", default="false").lower() == "true"
    new_appt = AppointmentService.schedule_appointment(payload, allow_past=allow_past)
    return api_success(data=new_appt, message="Appointment scheduled successfully", status_code=201)


@appointments_bp.route("/<int:appointment_id>", methods=["GET"])
def get_appointment(appointment_id: int):
    """
    GET /api/appointments/<appointment_id>
    Retrieves a single appointment by ID.
    """
    appt = AppointmentService.get_appointment(appointment_id)
    return api_success(data=appt, message="Appointment retrieved successfully")


@appointments_bp.route("/<int:appointment_id>/cancel", methods=["PUT"])
def cancel_appointment(appointment_id: int):
    """
    PUT /api/appointments/<appointment_id>/cancel
    Cancels an appointment with a required cancellation reason.
    """
    payload = request.get_json() or {}
    reason = payload.get("cancellation_reason") or payload.get("reason", "")
    cancelled = AppointmentService.cancel_appointment(appointment_id, reason)
    return api_success(data=cancelled, message="Appointment cancelled successfully")
