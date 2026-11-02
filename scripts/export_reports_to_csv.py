"""
CSV Reporting and Tableau Dataset Generator
Exports database queries into structured CSV files for Tableau Public and operational distribution.
"""

import sys
import shutil
from pathlib import Path
import pandas as pd

# Add root directory to python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app.repositories.db import db
from app.services.report_service import ReportService
from app.utils.logger import logger

REPORTS_DIR = ROOT_DIR / "reports" / "exports"
TABLEAU_DIR = ROOT_DIR / "tableau" / "exports"


def generate_exports():
    """Generates all 5 operational report CSVs and the unified Tableau master dataset."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    TABLEAU_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("Generating operational report exports...")

    # 1. Monthly Billing Summary
    billing_data = ReportService.get_monthly_billing_summary(year=2026)
    df_billing = pd.DataFrame(billing_data)
    billing_path = REPORTS_DIR / "monthly_billing_summary.csv"
    df_billing.to_csv(billing_path, index=False)
    logger.info(f"Exported Monthly Billing Summary: {len(df_billing)} rows")

    # 2. Appointment Status Summary
    appt_status = ReportService.get_appointment_status_report()
    df_dept = pd.DataFrame(appt_status["department_breakdown"])
    dept_path = REPORTS_DIR / "appointment_status_summary.csv"
    df_dept.to_csv(dept_path, index=False)
    logger.info(f"Exported Appointment Status Breakdown: {len(df_dept)} rows")

    # 3. Patient Visit History (Comprehensive patient visit records)
    history_sql = """
        SELECT 
            p.patient_id,
            p.patient_mrn,
            p.first_name || ' ' || p.last_name AS patient_name,
            p.date_of_birth,
            p.gender,
            p.blood_group,
            e.encounter_id,
            e.encounter_date,
            e.encounter_type,
            e.chief_complaint,
            e.diagnosis_code,
            e.diagnosis_description,
            pr.first_name || ' ' || pr.last_name AS attending_provider,
            pr.department,
            pr.specialty,
            b.bill_number,
            b.total_amount,
            b.paid_amount,
            b.balance_due,
            b.status AS billing_status
        FROM ENCOUNTERS e
        JOIN PATIENTS p ON e.patient_id = p.patient_id
        JOIN PROVIDERS pr ON e.provider_id = pr.provider_id
        LEFT JOIN BILLING_RECORDS b ON e.encounter_id = b.encounter_id
        ORDER BY e.encounter_date DESC
    """
    history_rows = db.execute_query(history_sql)
    df_history = pd.DataFrame(history_rows)
    history_path = REPORTS_DIR / "patient_visit_history.csv"
    df_history.to_csv(history_path, index=False)
    logger.info(f"Exported Patient Visit History: {len(df_history)} rows")

    # 4. Provider Utilization Summary
    provider_data = ReportService.get_provider_utilization_report()
    df_provider = pd.DataFrame(provider_data)
    provider_path = REPORTS_DIR / "provider_utilization_summary.csv"
    df_provider.to_csv(provider_path, index=False)
    logger.info(f"Exported Provider Utilization Summary: {len(df_provider)} rows")

    # 5. Outstanding Billing Aging Summary
    aging_data = ReportService.get_outstanding_billing_report()
    df_aging = pd.DataFrame(aging_data["overdue_invoices"])
    aging_path = REPORTS_DIR / "outstanding_billing_summary.csv"
    df_aging.to_csv(aging_path, index=False)
    logger.info(f"Exported Outstanding Billing Summary: {len(df_aging)} rows")

    # 6. Master Unified Tableau Dataset (Denormalized)
    master_sql = """
        SELECT 
            a.appointment_id,
            a.appointment_date,
            a.appointment_time,
            a.appointment_datetime,
            a.duration_minutes,
            a.reason_for_visit,
            a.status AS appointment_status,
            a.cancellation_reason,
            p.patient_id,
            p.patient_mrn,
            p.first_name || ' ' || p.last_name AS patient_name,
            p.gender AS patient_gender,
            p.date_of_birth AS patient_dob,
            pr.provider_id,
            pr.first_name || ' ' || pr.last_name AS provider_name,
            pr.department AS provider_department,
            pr.specialty AS provider_specialty,
            e.encounter_id,
            e.encounter_type,
            e.chief_complaint,
            e.diagnosis_code,
            e.diagnosis_description,
            b.bill_id,
            b.bill_number,
            b.billing_date,
            b.due_date,
            COALESCE(b.total_amount, 0.0) AS billed_amount,
            COALESCE(b.paid_amount, 0.0) AS paid_amount,
            COALESCE(b.balance_due, 0.0) AS balance_due,
            COALESCE(b.status, 'NO_BILL') AS billing_status,
            b.payment_method
        FROM APPOINTMENTS a
        JOIN PATIENTS p ON a.patient_id = p.patient_id
        JOIN PROVIDERS pr ON a.provider_id = pr.provider_id
        LEFT JOIN ENCOUNTERS e ON a.appointment_id = e.appointment_id
        LEFT JOIN BILLING_RECORDS b ON e.encounter_id = b.encounter_id
        ORDER BY a.appointment_datetime DESC
    """
    master_rows = db.execute_query(master_sql)
    df_master = pd.DataFrame(master_rows)
    master_path = REPORTS_DIR / "full_synthetic_dataset.csv"
    df_master.to_csv(master_path, index=False)
    logger.info(f"Exported Master Tableau Dataset: {len(df_master)} rows")

    # Copy files into tableau/exports
    for f in REPORTS_DIR.glob("*.csv"):
        shutil.copy(f, TABLEAU_DIR / f.name)
    logger.info(f"All reports copied to Tableau exports directory: {TABLEAU_DIR}")


if __name__ == "__main__":
    generate_exports()
