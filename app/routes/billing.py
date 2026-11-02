"""
Billing and Revenue REST API Endpoints
"""

from flask import Blueprint, request
from app.services.billing_service import BillingService
from app.utils.response import api_success, api_paginated

billing_bp = Blueprint("billing", __name__, url_prefix="/api/billing")


@billing_bp.route("", methods=["GET"])
def get_bills():
    """
    GET /api/billing
    Retrieves filtered list of billing invoices with pagination.
    """
    patient_id = request.args.get("patient_id", type=int)
    status = request.args.get("status", type=str)
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=20, type=int)

    items, total = BillingService.list_bills(
        patient_id=patient_id,
        status=status,
        page=page,
        page_size=page_size,
    )
    return api_paginated(items, total=total, page=page, page_size=page_size, message="Billing records retrieved successfully")


@billing_bp.route("", methods=["POST"])
def create_bill():
    """
    POST /api/billing
    Generates a new billing record.
    """
    payload = request.get_json() or {}
    new_bill = BillingService.create_bill(payload)
    return api_success(data=new_bill, message="Billing record created successfully", status_code=201)


@billing_bp.route("/<int:bill_id>", methods=["GET"])
def get_bill(bill_id: int):
    """
    GET /api/billing/<bill_id>
    Retrieves an invoice by ID.
    """
    bill = BillingService.get_bill(bill_id)
    return api_success(data=bill, message="Billing record retrieved successfully")


@billing_bp.route("/<int:bill_id>/payment", methods=["POST"])
def record_payment(bill_id: int):
    """
    POST /api/billing/<bill_id>/payment
    Records payment against an open invoice using exact decimal math.
    """
    payload = request.get_json() or {}
    payment_result = BillingService.process_payment(bill_id, payload)
    return api_success(data=payment_result, message="Payment applied successfully")
