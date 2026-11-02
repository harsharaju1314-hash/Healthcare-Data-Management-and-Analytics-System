"""
Operational Reporting and Analytics Service
Executes reporting workflows, generates CSV exports using Pandas,
and prepares data for Tableau visual integration.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
from app.repositories.report_repo import ReportRepository
from app.utils.logger import logger

EXPORTS_DIR = Path(__file__).resolve().parent.parent.parent / "reports" / "exports"


class ReportService:
    """Service layer for analytical and operational report generation."""

    @staticmethod
    def get_monthly_billing_summary(year: Optional[int] = None) -> List[Dict[str, Any]]:
        """Report 1: Monthly billing summary."""
        return ReportRepository.get_monthly_billing_summary(year)

    @staticmethod
    def get_appointment_status_report(start_date: Optional[str] = None,
                                      end_date: Optional[str] = None) -> Dict[str, Any]:
        """Report 2: Appointment status and cancellation report."""
        return ReportRepository.get_appointment_status_report(start_date, end_date)

    @staticmethod
    def get_patient_visit_history(patient_id: int) -> Dict[str, Any]:
        """Report 3: Patient visit timeline and encounter summary."""
        return ReportRepository.get_patient_visit_history(patient_id)

    @staticmethod
    def get_provider_utilization_report(start_date: Optional[str] = None,
                                        end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Report 4: Provider appointment utilization report."""
        return ReportRepository.get_provider_utilization_report(start_date, end_date)

    @staticmethod
    def get_outstanding_billing_report() -> Dict[str, Any]:
        """Report 5: Outstanding balances and aging report."""
        return ReportRepository.get_outstanding_billing_report()

    @staticmethod
    def get_dashboard_summary() -> Dict[str, Any]:
        """Calculates executive KPI summary cards for dashboard."""
        return ReportRepository.get_kpi_summary()

    @staticmethod
    def export_report_to_csv(report_name: str, records: List[Dict[str, Any]]) -> str:
        """
        Converts reporting dataset to CSV using Pandas and writes to reports/exports.
        Returns the absolute file path of the saved export.
        """
        EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
        file_path = EXPORTS_DIR / f"{report_name}.csv"

        df = pd.DataFrame(records)
        df.to_csv(file_path, index=False, encoding="utf-8")
        logger.info(f"Exported {len(records)} records for report '{report_name}' to {file_path}")
        return str(file_path)
