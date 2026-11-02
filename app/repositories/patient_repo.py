"""
Patient Data Repository
Handles CRUD operations, indexed searches, and persistence for Patient records.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from app.repositories.db import db
from app.utils.logger import logger


class PatientRepository:
    """Data access repository for PATIENTS table."""

    @staticmethod
    def get_next_mrn() -> str:
        """Generates the next sequential synthetic Medical Record Number."""
        sql = "SELECT MAX(patient_id) as max_id FROM PATIENTS"
        res = db.execute_one(sql)
        max_id = (res.get("max_id") or 0) + 1
        return f"MRN-{10000 + max_id}"

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        """Registers a new patient record."""
        mrn = data.get("patient_mrn") or PatientRepository.get_next_mrn()

        sql = """
            INSERT INTO PATIENTS (
                patient_mrn, first_name, last_name, date_of_birth,
                gender, blood_group, email, phone, address,
                emergency_contact_name, emergency_contact_phone, is_active
            ) VALUES (
                :patient_mrn, :first_name, :last_name, :date_of_birth,
                :gender, :blood_group, :email, :phone, :address,
                :emergency_contact_name, :emergency_contact_phone, :is_active
            )
        """
        params = {
            "patient_mrn": mrn,
            "first_name": data["first_name"].strip(),
            "last_name": data["last_name"].strip(),
            "date_of_birth": data["date_of_birth"],
            "gender": data["gender"],
            "blood_group": data.get("blood_group"),
            "email": data.get("email"),
            "phone": data["phone"].strip(),
            "address": data.get("address"),
            "emergency_contact_name": data.get("emergency_contact_name"),
            "emergency_contact_phone": data.get("emergency_contact_phone"),
            "is_active": data.get("is_active", 1),
        }
        _, last_id = db.execute_non_query(sql, params)
        if last_id:
            return last_id
        # For databases where lastrowid is not directly exposed, fetch by MRN
        rec = PatientRepository.get_by_mrn(mrn)
        return rec["patient_id"] if rec else 0

    @staticmethod
    def get_by_id(patient_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a patient by primary key."""
        sql = "SELECT * FROM PATIENTS WHERE patient_id = :patient_id"
        return db.execute_one(sql, {"patient_id": patient_id})

    @staticmethod
    def get_by_mrn(patient_mrn: str) -> Optional[Dict[str, Any]]:
        """Retrieves a patient by unique Medical Record Number."""
        sql = "SELECT * FROM PATIENTS WHERE patient_mrn = :patient_mrn"
        return db.execute_one(sql, {"patient_mrn": patient_mrn})

    @staticmethod
    def get_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Retrieves a patient by email address."""
        if not email:
            return None
        sql = "SELECT * FROM PATIENTS WHERE LOWER(email) = LOWER(:email)"
        return db.execute_one(sql, {"email": email.strip()})

    @staticmethod
    def search(search_term: Optional[str] = None, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """Searches patients by name or MRN with pagination."""
        if search_term:
            term = f"%{search_term.strip().lower()}%"
            sql = """
                SELECT * FROM PATIENTS
                WHERE LOWER(first_name) LIKE :term 
                   OR LOWER(last_name) LIKE :term
                   OR LOWER(patient_mrn) LIKE :term
                   OR LOWER(phone) LIKE :term
                ORDER BY last_name, first_name
                LIMIT :limit OFFSET :offset
            """
            params = {"term": term, "limit": limit, "offset": offset}
        else:
            sql = """
                SELECT * FROM PATIENTS
                ORDER BY patient_id DESC
                LIMIT :limit OFFSET :offset
            """
            params = {"limit": limit, "offset": offset}

        return db.execute_query(sql, params)

    @staticmethod
    def count(search_term: Optional[str] = None) -> int:
        """Counts total patient records matching search term."""
        if search_term:
            term = f"%{search_term.strip().lower()}%"
            sql = """
                SELECT COUNT(*) as total FROM PATIENTS
                WHERE LOWER(first_name) LIKE :term 
                   OR LOWER(last_name) LIKE :term
                   OR LOWER(patient_mrn) LIKE :term
                   OR LOWER(phone) LIKE :term
            """
            res = db.execute_one(sql, {"term": term})
        else:
            sql = "SELECT COUNT(*) as total FROM PATIENTS"
            res = db.execute_one(sql)

        return res.get("total", 0) if res else 0

    @staticmethod
    def update(patient_id: int, data: Dict[str, Any]) -> bool:
        """Updates an existing patient's details."""
        fields = []
        params = {"patient_id": patient_id}
        for k in ["first_name", "last_name", "date_of_birth", "gender", "blood_group",
                  "email", "phone", "address", "emergency_contact_name", "emergency_contact_phone", "is_active"]:
            if k in data:
                fields.append(f"{k} = :{k}")
                params[k] = data[k]

        if not fields:
            return False

        fields.append("updated_at = :updated_at")
        params["updated_at"] = datetime.now().isoformat()

        sql = f"UPDATE PATIENTS SET {', '.join(fields)} WHERE patient_id = :patient_id"
        rowcount, _ = db.execute_non_query(sql, params)
        return rowcount > 0

    @staticmethod
    def soft_delete(patient_id: int) -> bool:
        """Deactivates a patient record without deleting clinical history."""
        sql = "UPDATE PATIENTS SET is_active = 0, updated_at = :updated_at WHERE patient_id = :patient_id"
        rowcount, _ = db.execute_non_query(sql, {
            "patient_id": patient_id,
            "updated_at": datetime.now().isoformat()
        })
        return rowcount > 0
