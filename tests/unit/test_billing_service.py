"""
Unit Tests for Billing Service Workflows
"""

import pytest
from app.services.billing_service import BillingService
from app.utils.exceptions import ValidationException, ConflictException, ResourceNotFoundException


def test_create_bill_success(client):
    # Patient 4 has encounter without a bill (or let's use Patient 2)
    # Encounters in seed data: 1 to 22. Encounter 22 is for patient 25.
    # Let's check non-existent encounter
    with pytest.raises(ResourceNotFoundException):
        BillingService.create_bill({
            "patient_id": 1,
            "encounter_id": 9999,
            "total_amount": 150.00
        })


def test_apply_payment_success(client):
    # Bill 4 is PARTIALLY_PAID (Total 400.00, Paid 200.00, Balance 200.00)
    res = BillingService.process_payment(4, {
        "payment_amount": 100.00,
        "payment_method": "CREDIT_CARD",
    })
    assert res["paid_amount"] == 300.00
    assert res["balance_due"] == 100.00
    assert res["status"] == "PARTIALLY_PAID"

    # Now pay remaining 100.00
    res_final = BillingService.process_payment(4, {
        "payment_amount": 100.00,
        "payment_method": "CREDIT_CARD",
    })
    assert res_final["balance_due"] == 0.00
    assert res_final["status"] == "PAID"


def test_apply_overpayment_fails(client):
    # Bill 10 is OVERDUE (Balance 175.00)
    with pytest.raises(ValidationException) as exc:
        BillingService.process_payment(10, {
            "payment_amount": 500.00,
            "payment_method": "CASH",
        })
    assert "exceeds remaining balance" in str(exc.value)


def test_apply_payment_to_fully_paid_bill_fails(client):
    # Bill 1 is already PAID (Balance 0.00)
    with pytest.raises(ConflictException) as exc:
        BillingService.process_payment(1, {
            "payment_amount": 50.00,
            "payment_method": "CASH",
        })
    assert "already been paid in full" in str(exc.value)


def test_patient_outstanding_balance_calculation(client):
    # Patient 5 has invoice 4 with balance 200.00 in seed data
    bal = BillingService.get_patient_outstanding_balance(5)
    assert bal["outstanding_balance"] == 200.00
