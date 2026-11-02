"""
Clinical Encounter Data Repository
Handles CRUD operations, diagnosis tracking, and clinical encounter notes persistence.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from app.repositories.db import db


class EncounterRepository:
    """Data access repository for ENCOUNTERS table."""

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        """Records a new clinical encounter."""
        now = datetime.now().isoformat()
        sql = """
            INSERT INTO ENCOUNTERS (
                appointment_id, patient_id, provider_id,
                encounter_type, encounter_date, chief_complaint,
                clinical_notes, diagnosis_code, diagnosis_description, status
            ) VALUES (
                :appointment_id, :patient_id, :provider_id,
                :encounter_type, :encounter_date, :chief_complaint,
                :clinical_notes, :diagnosis_code, :diagnosis_description, :status
            )
        """
        params = {
            "appointment_id": data.get("appointment_id"),
            "patient_id": data["patient_id"],
            "provider_id": data["provider_id"],
            "encounter_type": data.get("encounter_type", "OUTPATIENT"),
            "encounter_date": data.get("encounter_date", now),
            "chief_complaint": data["chief_complaint"].strip(),
            "clinical_notes": data["clinical_notes"].strip(),
            "diagnosis_code": data["diagnosis_code"].strip().upper(),
            "diagnosis_description": data["diagnosis_description"].strip(),
            "status": data.get("status", "COMPLETED"),
        }
        _, last_id = db.execute_non_query(sql, params)
        if last_id:
            return last_id

        # Query fallback
        res = db.execute_one(
            "SELECT MAX(encounter_id) as max_id FROM ENCOUNTERS WHERE patient_id = :p",
            {"p": data["patient_id"]}
        )
        return res["max_id"] if res else 0

    @staticmethod
    def get_by_id(encounter_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves clinical encounter details with patient, provider, and billing info."""
        sql = """
            SELECT 
                e.*,
                p.patient_mrn,
                p.first_name || ' ' || p.last_name AS patient_name,
                pr.first_name || ' ' || pr.last_name AS provider_name,
                pr.specialty AS provider_specialty,
                b.bill_id,
                b.bill_number,
                b.total_amount AS billed_total,
                b.balance_due,
                b.status AS billing_status
            FROM ENCOUNTERS e
            JOIN PATIENTS p ON e.patient_id = p.patient_id
            JOIN PROVIDERS pr ON e.provider_id = pr.provider_id
            LEFT JOIN BILLING_RECORDS b ON e.encounter_id = b.encounter_id
            WHERE e.encounter_id = :encounter_id
        """
        return db.execute_one(sql, {"encounter_id": encounter_id})

    @staticmethod
    def get_list(patient_id: Optional[int] = None,
                 provider_id: Optional[int] = None,
                 encounter_type: Optional[str] = None,
                 limit: int = 20,
                 offset: int = 0) -> List[Dict[str, Any]]:
        """Retrieves paginated list of clinical encounters."""
        conditions = []
        params = {"limit": limit, "offset": offset}

        if patient_id:
            conditions.append("e.patient_id = :patient_id")
            params["patient_id"] = patient_id
        if provider_id:
            conditions.append("e.provider_id = :provider_id")
            params["provider_id"] = provider_id
        if encounter_type:
            conditions.append("e.encounter_type = :encounter_type")
            params["encounter_type"] = encounter_type.upper()

        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

        sql = f"""
            SELECT 
                e.*,
                p.patient_mrn,
                p.first_name || ' ' || p.last_name AS patient_name,
                pr.first_name || ' ' || pr.last_name AS provider_name,
                pr.specialty AS provider_specialty
            FROM ENCOUNTERS e
            JOIN PATIENTS p ON e.patient_id = p.patient_id
            JOIN PROVIDERS pr ON e.provider_id = pr.provider_id
            {where_clause}
            ORDER BY e.encounter_date DESC
            LIMIT :limit OFFSET :offset
        """
        return db.execute_query(sql, params)

    @staticmethod
    def count(patient_id: Optional[int] = None,
              provider_id: Optional[int] = None,
              encounter_type: Optional[str] = None) -> int:
        """Counts clinical encounters matching filter criteria."""
        conditions = []
        params = {}

        if patient_id:
            conditions.append("patient_id = :patient_id")
            params["patient_id"] = patient_id
        if provider_id:
            conditions.append("provider_id = :provider_id")
            params["provider_id"] = provider_id
        if encounter_type:
            conditions.append("encounter_type = :encounter_type")
            params["encounter_type"] = encounter_type.upper()

        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        sql = f"SELECT COUNT(*) as total FROM ENCOUNTERS {where_clause}"
        res = db.execute_one(sql, params)
        return res.get("total", 0) if res else 0
