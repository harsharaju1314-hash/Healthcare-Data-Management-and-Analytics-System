"""
Healthcare Provider Repository
Data access methods for PROVIDERS table.
"""

from typing import List, Dict, Any, Optional
from app.repositories.db import db


class ProviderRepository:
    """Data access repository for PROVIDERS table."""

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Retrieves all providers ordered by department and name."""
        sql = "SELECT * FROM PROVIDERS ORDER BY department, last_name, first_name"
        return db.execute_query(sql)

    @staticmethod
    def get_by_id(provider_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves provider by primary key."""
        sql = "SELECT * FROM PROVIDERS WHERE provider_id = :provider_id"
        return db.execute_one(sql, {"provider_id": provider_id})

    @staticmethod
    def get_by_department(department: str) -> List[Dict[str, Any]]:
        """Filters providers by clinical department."""
        sql = "SELECT * FROM PROVIDERS WHERE LOWER(department) = LOWER(:dept) ORDER BY last_name"
        return db.execute_query(sql, {"dept": department.strip()})
