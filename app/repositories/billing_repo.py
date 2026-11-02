"""
Billing Data Repository
Handles CRUD operations, exact decimal payment applications, and balance calculations.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
from app.repositories.db import db
from app.utils.decimal_utils import to_decimal, calculate_balance, validate_billing_math
from app.utils.exceptions import ValidationException, ConflictException, ResourceNotFoundException


class BillingRepository:
    """Data access repository for BILLING_RECORDS table."""

    @staticmethod
    def generate_bill_number() -> str:
        """Generates a unique invoice number: INV-YYYYMMDD-XXXXX."""
        today_str = date.today().strftime("%Y%m%d")
        sql = "SELECT COUNT(*) as cnt FROM BILLING_RECORDS WHERE bill_number LIKE :prefix"
        res = db.execute_one(sql, {"prefix": f"INV-{today_str}%"})
        seq = (res.get("cnt") or 0) + 1
        return f"INV-{today_str}-{seq:05d}"

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        """Creates a new billing invoice."""
        total = to_decimal(data["total_amount"])
        paid = to_decimal(data.get("paid_amount", "0.00"))
        balance = calculate_balance(total, paid)

        is_valid, msg = validate_billing_math(total, paid, balance)
        if not is_valid:
            raise ValidationException(f"Billing calculation error: {msg}")

        bill_num = data.get("bill_number") or BillingRepository.generate_bill_number()
        today = date.today()
        due = data.get("due_date") or (today + timedelta(days=30)).isoformat()
        status = "PAID" if balance == Decimal("0.00") else ("PARTIALLY_PAID" if paid > Decimal("0.00") else "PENDING")

        sql = """
            INSERT INTO BILLING_RECORDS (
                bill_number, patient_id, encounter_id,
                billing_date, due_date, total_amount,
                paid_amount, balance_due, status, payment_method
            ) VALUES (
                :bill_number, :patient_id, :encounter_id,
                :billing_date, :due_date, :total_amount,
                :paid_amount, :balance_due, :status, :payment_method
            )
        """
        params = {
            "bill_number": bill_num,
            "patient_id": data["patient_id"],
            "encounter_id": data["encounter_id"],
            "billing_date": data.get("billing_date", today.isoformat()),
            "due_date": due,
            "total_amount": float(total),
            "paid_amount": float(paid),
            "balance_due": float(balance),
            "status": status,
            "payment_method": data.get("payment_method"),
        }
        _, last_id = db.execute_non_query(sql, params)
        if last_id:
            return last_id

        rec = BillingRepository.get_by_number(bill_num)
        return rec["bill_id"] if rec else 0

    @staticmethod
    def get_by_id(bill_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a billing record by primary key."""
        sql = """
            SELECT 
                b.*,
                p.patient_mrn,
                p.first_name || ' ' || p.last_name AS patient_name,
                e.encounter_type,
                e.diagnosis_code,
                e.diagnosis_description
            FROM BILLING_RECORDS b
            JOIN PATIENTS p ON b.patient_id = p.patient_id
            JOIN ENCOUNTERS e ON b.encounter_id = e.encounter_id
            WHERE b.bill_id = :bill_id
        """
        return db.execute_one(sql, {"bill_id": bill_id})

    @staticmethod
    def get_by_number(bill_number: str) -> Optional[Dict[str, Any]]:
        """Retrieves an invoice by bill number."""
        sql = "SELECT * FROM BILLING_RECORDS WHERE bill_number = :bill_number"
        return db.execute_one(sql, {"bill_number": bill_number})

    @staticmethod
    def get_by_encounter_id(encounter_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves billing invoice for an encounter."""
        sql = "SELECT * FROM BILLING_RECORDS WHERE encounter_id = :encounter_id"
        return db.execute_one(sql, {"encounter_id": encounter_id})

    @staticmethod
    def get_list(patient_id: Optional[int] = None,
                 status: Optional[str] = None,
                 limit: int = 20,
                 offset: int = 0) -> List[Dict[str, Any]]:
        """Retrieves paginated list of billing invoices."""
        conditions = []
        params = {"limit": limit, "offset": offset}

        if patient_id:
            conditions.append("b.patient_id = :patient_id")
            params["patient_id"] = patient_id
        if status:
            conditions.append("b.status = :status")
            params["status"] = status.upper()

        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

        sql = f"""
            SELECT 
                b.*,
                p.patient_mrn,
                p.first_name || ' ' || p.last_name AS patient_name
            FROM BILLING_RECORDS b
            JOIN PATIENTS p ON b.patient_id = p.patient_id
            {where_clause}
            ORDER BY b.billing_date DESC
            LIMIT :limit OFFSET :offset
        """
        return db.execute_query(sql, params)

    @staticmethod
    def count(patient_id: Optional[int] = None, status: Optional[str] = None) -> int:
        """Counts billing records matching filter criteria."""
        conditions = []
        params = {}

        if patient_id:
            conditions.append("patient_id = :patient_id")
            params["patient_id"] = patient_id
        if status:
            conditions.append("status = :status")
            params["status"] = status.upper()

        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        sql = f"SELECT COUNT(*) as total FROM BILLING_RECORDS {where_clause}"
        res = db.execute_one(sql, params)
        return res.get("total", 0) if res else 0

    @staticmethod
    def apply_payment(bill_id: int, payment_amount: Decimal, payment_method: str) -> Dict[str, Any]:
        """
        Applies a payment to an open invoice with strict monetary validation.
        Transitions status to PAID or PARTIALLY_PAID.
        """
        bill = BillingRepository.get_by_id(bill_id)
        if not bill:
            raise ResourceNotFoundException(f"Invoice ID {bill_id} not found.")

        if bill["status"] == "CANCELLED":
            raise ConflictException("Cannot apply payment to a cancelled invoice.")

        current_balance = to_decimal(bill["balance_due"])
        if current_balance <= Decimal("0.00"):
            raise ConflictException("Invoice has already been paid in full.")

        if payment_amount <= Decimal("0.00"):
            raise ValidationException("Payment amount must be greater than zero.")

        if payment_amount > current_balance:
            raise ValidationException(
                f"Payment amount (${payment_amount}) exceeds remaining balance (${current_balance})."
            )

        current_paid = to_decimal(bill["paid_amount"])
        new_paid = current_paid + payment_amount
        new_balance = current_balance - payment_amount
        new_status = "PAID" if new_balance == Decimal("0.00") else "PARTIALLY_PAID"

        sql = """
            UPDATE BILLING_RECORDS
            SET paid_amount = :paid_amount,
                balance_due = :balance_due,
                status = :status,
                payment_method = :payment_method,
                updated_at = :updated_at
            WHERE bill_id = :bill_id
        """
        params = {
            "bill_id": bill_id,
            "paid_amount": float(new_paid),
            "balance_due": float(new_balance),
            "status": new_status,
            "payment_method": payment_method,
            "updated_at": datetime.now().isoformat(),
        }
        db.execute_non_query(sql, params)

        return {
            "bill_id": bill_id,
            "bill_number": bill["bill_number"],
            "total_amount": float(to_decimal(bill["total_amount"])),
            "paid_amount": float(new_paid),
            "balance_due": float(new_balance),
            "status": new_status,
            "payment_applied": float(payment_amount),
        }

    @staticmethod
    def get_patient_balance(patient_id: int) -> Decimal:
        """Calculates total outstanding balance for a patient across all active bills."""
        sql = """
            SELECT SUM(balance_due) as total_balance
            FROM BILLING_RECORDS
            WHERE patient_id = :patient_id
              AND status IN ('PENDING', 'PARTIALLY_PAID', 'OVERDUE')
        """
        res = db.execute_one(sql, {"patient_id": patient_id})
        return to_decimal(res.get("total_balance", 0.00))
