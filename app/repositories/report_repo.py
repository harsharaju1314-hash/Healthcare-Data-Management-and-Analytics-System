"""
Operational Reports and Analytics Repository
Executes SQL queries for operational reporting, dashboard metrics, and analytical summaries.
"""

from typing import List, Dict, Any, Optional
from datetime import date
from app.repositories.db import db


class ReportRepository:
    """Data access repository for operational reports and KPIs."""

    @staticmethod
    def get_monthly_billing_summary(year: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Report 1: Monthly Billing Summary
        Aggregates billings, collections, outstanding balances, and collection efficiency.
        """
        year_filter = year or date.today().year

        sql = """
            SELECT 
                SUBSTR(billing_date, 1, 7) AS billing_month,
                COUNT(bill_id) AS total_bills,
                ROUND(SUM(total_amount), 2) AS total_billed,
                ROUND(SUM(paid_amount), 2) AS total_collected,
                ROUND(SUM(balance_due), 2) AS total_outstanding,
                ROUND(CASE WHEN SUM(total_amount) > 0 
                      THEN (SUM(paid_amount) * 100.0 / SUM(total_amount)) 
                      ELSE 0 END, 2) AS collection_rate_pct,
                COUNT(CASE WHEN status = 'PAID' THEN 1 END) AS paid_count,
                COUNT(CASE WHEN status IN ('PENDING', 'PARTIALLY_PAID') THEN 1 END) AS pending_count,
                COUNT(CASE WHEN status = 'OVERDUE' THEN 1 END) AS overdue_count
            FROM BILLING_RECORDS
            WHERE billing_date LIKE :year_pattern
              AND status != 'CANCELLED'
            GROUP BY SUBSTR(billing_date, 1, 7)
            ORDER BY billing_month ASC
        """
        return db.execute_query(sql, {"year_pattern": f"{year_filter}%"})

    @staticmethod
    def get_appointment_status_report(start_date: Optional[str] = None,
                                      end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Report 2: Appointment Status and Cancellation Report
        Breaks down appointment volume by status, cancellation reasons, and departments.
        """
        conditions = []
        params = {}
        if start_date:
            conditions.append("a.appointment_date >= :start_date")
            params["start_date"] = start_date
        if end_date:
            conditions.append("a.appointment_date <= :end_date")
            params["end_date"] = end_date

        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

        # Status distribution query
        status_sql = f"""
            SELECT 
                a.status,
                COUNT(*) AS count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM APPOINTMENTS a {where_clause}), 2) AS percentage
            FROM APPOINTMENTS a
            {where_clause}
            GROUP BY a.status
            ORDER BY count DESC
        """
        status_summary = db.execute_query(status_sql, params)

        # Department breakdown query
        dept_sql = f"""
            SELECT 
                pr.department,
                COUNT(a.appointment_id) AS total_scheduled,
                COUNT(CASE WHEN a.status = 'COMPLETED' THEN 1 END) AS completed,
                COUNT(CASE WHEN a.status = 'CANCELLED' THEN 1 END) AS cancelled,
                COUNT(CASE WHEN a.status = 'NO_SHOW' THEN 1 END) AS no_show,
                ROUND(CASE WHEN COUNT(a.appointment_id) > 0 
                      THEN (COUNT(CASE WHEN a.status = 'CANCELLED' THEN 1 END) * 100.0 / COUNT(a.appointment_id))
                      ELSE 0 END, 2) AS cancellation_rate_pct
            FROM APPOINTMENTS a
            JOIN PROVIDERS pr ON a.provider_id = pr.provider_id
            {where_clause}
            GROUP BY pr.department
            ORDER BY total_scheduled DESC
        """
        dept_summary = db.execute_query(dept_sql, params)

        # Cancellation reasons query
        cancel_sql = f"""
            SELECT 
                COALESCE(cancellation_reason, 'Unspecified') AS reason,
                COUNT(*) AS count
            FROM APPOINTMENTS a
            {where_clause} {"AND" if where_clause else "WHERE"} status = 'CANCELLED'
            GROUP BY cancellation_reason
            ORDER BY count DESC
        """
        cancellation_reasons = db.execute_query(cancel_sql, params)

        return {
            "status_distribution": status_summary,
            "department_breakdown": dept_summary,
            "cancellation_reasons": cancellation_reasons,
        }

    @staticmethod
    def get_patient_visit_history(patient_id: int) -> Dict[str, Any]:
        """
        Report 3: Patient Visit History
        Complete chronological medical timeline for a single patient with encounters and billing.
        """
        patient_sql = "SELECT * FROM PATIENTS WHERE patient_id = :patient_id"
        patient = db.execute_one(patient_sql, {"patient_id": patient_id})

        timeline_sql = """
            SELECT 
                e.encounter_id,
                e.encounter_date,
                e.encounter_type,
                e.chief_complaint,
                e.clinical_notes,
                e.diagnosis_code,
                e.diagnosis_description,
                pr.first_name || ' ' || pr.last_name AS provider_name,
                pr.department,
                pr.specialty,
                b.bill_id,
                b.bill_number,
                b.total_amount,
                b.paid_amount,
                b.balance_due,
                b.status AS billing_status
            FROM ENCOUNTERS e
            JOIN PROVIDERS pr ON e.provider_id = pr.provider_id
            LEFT JOIN BILLING_RECORDS b ON e.encounter_id = b.encounter_id
            WHERE e.patient_id = :patient_id
            ORDER BY e.encounter_date DESC
        """
        timeline = db.execute_query(timeline_sql, {"patient_id": patient_id})

        return {
            "patient": patient,
            "encounters_count": len(timeline),
            "timeline": timeline,
        }

    @staticmethod
    def get_provider_utilization_report(start_date: Optional[str] = None,
                                        end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Report 4: Provider Appointment Utilization
        Measures clinical workload, completion ratios, unique patient reach, and billable output.
        """
        sql = """
            SELECT 
                pr.provider_id,
                pr.first_name || ' ' || pr.last_name AS provider_name,
                pr.department,
                pr.specialty,
                COUNT(a.appointment_id) AS total_appointments,
                COUNT(CASE WHEN a.status = 'COMPLETED' THEN 1 END) AS completed_appointments,
                COUNT(CASE WHEN a.status = 'CANCELLED' THEN 1 END) AS cancelled_appointments,
                COUNT(CASE WHEN a.status = 'NO_SHOW' THEN 1 END) AS no_show_appointments,
                COUNT(DISTINCT a.patient_id) AS unique_patients,
                ROUND(CASE WHEN COUNT(a.appointment_id) > 0 
                      THEN (COUNT(CASE WHEN a.status = 'COMPLETED' THEN 1 END) * 100.0 / COUNT(a.appointment_id))
                      ELSE 0 END, 2) AS completion_rate_pct,
                COUNT(DISTINCT e.encounter_id) AS clinical_encounters,
                ROUND(COALESCE(SUM(b.total_amount), 0), 2) AS total_revenue_generated
            FROM PROVIDERS pr
            LEFT JOIN APPOINTMENTS a ON pr.provider_id = a.provider_id
            LEFT JOIN ENCOUNTERS e ON pr.provider_id = e.provider_id
            LEFT JOIN BILLING_RECORDS b ON e.encounter_id = b.encounter_id AND b.status != 'CANCELLED'
            GROUP BY pr.provider_id, pr.first_name, pr.last_name, pr.department, pr.specialty
            ORDER BY total_appointments DESC
        """
        return db.execute_query(sql)

    @staticmethod
    def get_outstanding_billing_report() -> Dict[str, Any]:
        """
        Report 5: Outstanding Billing and Aging Report
        Categorizes overdue balances into aging buckets (Current, 1-30, 31-60, 61-90, 90+ days).
        """
        today = date.today().isoformat()

        aging_sql = f"""
            SELECT 
                CASE 
                    WHEN due_date >= '{today}' THEN 'Current'
                    WHEN (julianday('{today}') - julianday(due_date)) BETWEEN 1 AND 30 THEN '1-30 Days Overdue'
                    WHEN (julianday('{today}') - julianday(due_date)) BETWEEN 31 AND 60 THEN '31-60 Days Overdue'
                    WHEN (julianday('{today}') - julianday(due_date)) BETWEEN 61 AND 90 THEN '61-90 Days Overdue'
                    ELSE '90+ Days Overdue'
                END AS aging_bucket,
                COUNT(*) AS invoice_count,
                ROUND(SUM(balance_due), 2) AS total_outstanding
            FROM BILLING_RECORDS
            WHERE balance_due > 0 AND status IN ('PENDING', 'PARTIALLY_PAID', 'OVERDUE')
            GROUP BY aging_bucket
            ORDER BY total_outstanding DESC
        """
        aging_summary = db.execute_query(aging_sql)

        records_sql = """
            SELECT 
                b.bill_id,
                b.bill_number,
                b.patient_id,
                p.patient_mrn,
                p.first_name || ' ' || p.last_name AS patient_name,
                p.phone AS patient_phone,
                p.email AS patient_email,
                b.billing_date,
                b.due_date,
                b.total_amount,
                b.paid_amount,
                b.balance_due,
                b.status
            FROM BILLING_RECORDS b
            JOIN PATIENTS p ON b.patient_id = p.patient_id
            WHERE b.balance_due > 0 AND b.status IN ('PENDING', 'PARTIALLY_PAID', 'OVERDUE')
            ORDER BY b.due_date ASC
            LIMIT 50
        """
        detailed_invoices = db.execute_query(records_sql)

        total_due = sum(item.get("total_outstanding", 0) for item in aging_summary)

        return {
            "total_outstanding_amount": round(total_due, 2),
            "aging_distribution": aging_summary,
            "overdue_invoices": detailed_invoices,
        }

    @staticmethod
    def get_kpi_summary() -> Dict[str, Any]:
        """Dashboard overview metrics (KPI cards)."""
        stats_sql = """
            SELECT 
                (SELECT COUNT(*) FROM PATIENTS WHERE is_active = 1) AS total_patients,
                (SELECT COUNT(*) FROM PROVIDERS) AS total_providers,
                (SELECT COUNT(*) FROM APPOINTMENTS) AS total_appointments,
                (SELECT COUNT(*) FROM APPOINTMENTS WHERE status = 'COMPLETED') AS completed_appointments,
                (SELECT COUNT(*) FROM APPOINTMENTS WHERE status = 'CANCELLED') AS cancelled_appointments,
                (SELECT COUNT(*) FROM ENCOUNTERS) AS total_encounters,
                (SELECT ROUND(COALESCE(SUM(paid_amount), 0), 2) FROM BILLING_RECORDS WHERE status != 'CANCELLED') AS total_revenue_collected,
                (SELECT ROUND(COALESCE(SUM(balance_due), 0), 2) FROM BILLING_RECORDS WHERE status IN ('PENDING', 'PARTIALLY_PAID', 'OVERDUE')) AS total_outstanding_balance
        """
        res = db.execute_one(stats_sql) or {}
        tot_appts = res.get("total_appointments", 0)
        completed = res.get("completed_appointments", 0)
        cancelled = res.get("cancelled_appointments", 0)

        res["completion_rate_pct"] = round((completed * 100.0 / tot_appts), 2) if tot_appts > 0 else 0.0
        res["cancellation_rate_pct"] = round((cancelled * 100.0 / tot_appts), 2) if tot_appts > 0 else 0.0
        return res
