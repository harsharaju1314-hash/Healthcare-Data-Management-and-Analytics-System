"""
Appointment Data Repository
Handles CRUD operations, conflict checks, status transitions, and appointment history.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from app.repositories.db import db
from app.utils.logger import logger


class AppointmentRepository:
    """Data access repository for APPOINTMENTS table."""

    @staticmethod
    def check_conflict(provider_id: int, appointment_datetime: str, exclude_id: Optional[int] = None) -> bool:
        """
        Checks if the provider already has a non-cancelled appointment at the given datetime slot.
        Returns True if a conflict exists, False otherwise.
        """
        sql = """
            SELECT appointment_id FROM APPOINTMENTS
            WHERE provider_id = :provider_id
              AND appointment_datetime = :appointment_datetime
              AND status NOT IN ('CANCELLED')
        """
        params = {
            "provider_id": provider_id,
            "appointment_datetime": appointment_datetime,
        }
        if exclude_id:
            sql += " AND appointment_id != :exclude_id"
            params["exclude_id"] = exclude_id

        res = db.execute_one(sql, params)
        return res is not None

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        """Schedules a new appointment."""
        appt_dt = f"{data['appointment_date']} {data['appointment_time']}:00"

        sql = """
            INSERT INTO APPOINTMENTS (
                patient_id, provider_id, appointment_date,
                appointment_time, appointment_datetime, duration_minutes,
                reason_for_visit, status
            ) VALUES (
                :patient_id, :provider_id, :appointment_date,
                :appointment_time, :appointment_datetime, :duration_minutes,
                :reason_for_visit, :status
            )
        """
        params = {
            "patient_id": data["patient_id"],
            "provider_id": data["provider_id"],
            "appointment_date": data["appointment_date"],
            "appointment_time": data["appointment_time"],
            "appointment_datetime": appt_dt,
            "duration_minutes": data.get("duration_minutes", 30),
            "reason_for_visit": data["reason_for_visit"].strip(),
            "status": data.get("status", "SCHEDULED"),
        }
        _, last_id = db.execute_non_query(sql, params)
        if last_id:
            return last_id

        # Query fallback
        res = db.execute_one(
            "SELECT appointment_id FROM APPOINTMENTS WHERE provider_id = :p AND appointment_datetime = :dt",
            {"p": data["provider_id"], "dt": appt_dt}
        )
        return res["appointment_id"] if res else 0

    @staticmethod
    def get_by_id(appointment_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves an appointment with associated patient and provider names."""
        sql = """
            SELECT 
                a.*,
                p.patient_mrn,
                p.first_name || ' ' || p.last_name AS patient_name,
                p.phone AS patient_phone,
                pr.first_name || ' ' || pr.last_name AS provider_name,
                pr.specialty AS provider_specialty,
                pr.department AS provider_department
            FROM APPOINTMENTS a
            JOIN PATIENTS p ON a.patient_id = p.patient_id
            JOIN PROVIDERS pr ON a.provider_id = pr.provider_id
            WHERE a.appointment_id = :appointment_id
        """
        return db.execute_one(sql, {"appointment_id": appointment_id})

    @staticmethod
    def get_list(patient_id: Optional[int] = None,
                 provider_id: Optional[int] = None,
                 status: Optional[str] = None,
                 start_date: Optional[str] = None,
                 end_date: Optional[str] = None,
                 limit: int = 20,
                 offset: int = 0) -> List[Dict[str, Any]]:
        """Retrieves filtered list of appointments with pagination."""
        conditions = []
        params = {"limit": limit, "offset": offset}

        if patient_id:
            conditions.append("a.patient_id = :patient_id")
            params["patient_id"] = patient_id
        if provider_id:
            conditions.append("a.provider_id = :provider_id")
            params["provider_id"] = provider_id
        if status:
            conditions.append("a.status = :status")
            params["status"] = status.upper()
        if start_date:
            conditions.append("a.appointment_date >= :start_date")
            params["start_date"] = start_date
        if end_date:
            conditions.append("a.appointment_date <= :end_date")
            params["end_date"] = end_date

        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

        sql = f"""
            SELECT 
                a.*,
                p.patient_mrn,
                p.first_name || ' ' || p.last_name AS patient_name,
                pr.first_name || ' ' || pr.last_name AS provider_name,
                pr.specialty AS provider_specialty
            FROM APPOINTMENTS a
            JOIN PATIENTS p ON a.patient_id = p.patient_id
            JOIN PROVIDERS pr ON a.provider_id = pr.provider_id
            {where_clause}
            ORDER BY a.appointment_datetime DESC
            LIMIT :limit OFFSET :offset
        """
        return db.execute_query(sql, params)

    @staticmethod
    def count(patient_id: Optional[int] = None,
              provider_id: Optional[int] = None,
              status: Optional[str] = None,
              start_date: Optional[str] = None,
              end_date: Optional[str] = None) -> int:
        """Counts appointments matching filter criteria."""
        conditions = []
        params = {}

        if patient_id:
            conditions.append("patient_id = :patient_id")
            params["patient_id"] = patient_id
        if provider_id:
            conditions.append("provider_id = :provider_id")
            params["provider_id"] = provider_id
        if status:
            conditions.append("status = :status")
            params["status"] = status.upper()
        if start_date:
            conditions.append("appointment_date >= :start_date")
            params["start_date"] = start_date
        if end_date:
            conditions.append("appointment_date <= :end_date")
            params["end_date"] = end_date

        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        sql = f"SELECT COUNT(*) as total FROM APPOINTMENTS {where_clause}"
        res = db.execute_one(sql, params)
        return res.get("total", 0) if res else 0

    @staticmethod
    def cancel(appointment_id: int, reason: str) -> bool:
        """Marks an appointment as CANCELLED with cancellation reason."""
        now = datetime.now().isoformat()
        sql = """
            UPDATE APPOINTMENTS
            SET status = 'CANCELLED',
                cancellation_reason = :reason,
                cancelled_at = :cancelled_at,
                updated_at = :updated_at
            WHERE appointment_id = :appointment_id
        """
        rowcount, _ = db.execute_non_query(sql, {
            "appointment_id": appointment_id,
            "reason": reason.strip(),
            "cancelled_at": now,
            "updated_at": now,
        })
        return rowcount > 0

    @staticmethod
    def update_status(appointment_id: int, status: str) -> bool:
        """Updates appointment status."""
        sql = """
            UPDATE APPOINTMENTS
            SET status = :status, updated_at = :updated_at
            WHERE appointment_id = :appointment_id
        """
        rowcount, _ = db.execute_non_query(sql, {
            "appointment_id": appointment_id,
            "status": status.upper(),
            "updated_at": datetime.now().isoformat(),
        })
        return rowcount > 0
