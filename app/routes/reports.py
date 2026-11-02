"""
Operational Reports REST API Endpoints
"""

from flask import Blueprint, request, send_file
from app.services.report_service import ReportService
from app.utils.response import api_success
from app.utils.exceptions import ValidationException

reports_bp = Blueprint("reports", __name__, url_prefix="/api/reports")


@reports_bp.route("/monthly-billing", methods=["GET"])
def report_monthly_billing():
    """
    GET /api/reports/monthly-billing
    Report 1: Monthly billing totals, collections, and collection rates.
    """
    year = request.args.get("year", default=None, type=int)
    report = ReportService.get_monthly_billing_summary(year)
    return api_success(data=report, message="Monthly billing report generated")


@reports_bp.route("/appointment-status", methods=["GET"])
def report_appointment_status():
    """
    GET /api/reports/appointment-status
    Report 2: Appointment status breakdown and cancellation metrics.
    """
    start_date = request.args.get("start_date", type=str)
    end_date = request.args.get("end_date", type=str)
    report = ReportService.get_appointment_status_report(start_date, end_date)
    return api_success(data=report, message="Appointment status report generated")


@reports_bp.route("/patient-visit-history/<int:patient_id>", methods=["GET"])
def report_patient_visit_history(patient_id: int):
    """
    GET /api/reports/patient-visit-history/<patient_id>
    Report 3: Complete longitudinal patient visit timeline.
    """
    report = ReportService.get_patient_visit_history(patient_id)
    return api_success(data=report, message="Patient visit history generated")


@reports_bp.route("/provider-utilization", methods=["GET"])
def report_provider_utilization():
    """
    GET /api/reports/provider-utilization
    Report 4: Provider appointment utilization and revenue metrics.
    """
    start_date = request.args.get("start_date", type=str)
    end_date = request.args.get("end_date", type=str)
    report = ReportService.get_provider_utilization_report(start_date, end_date)
    return api_success(data=report, message="Provider utilization report generated")


@reports_bp.route("/outstanding-billing", methods=["GET"])
def report_outstanding_billing():
    """
    GET /api/reports/outstanding-billing
    Report 5: Outstanding invoices aging analysis.
    """
    report = ReportService.get_outstanding_billing_report()
    return api_success(data=report, message="Outstanding billing report generated")


@reports_bp.route("/export/<string:report_name>", methods=["GET"])
def export_report(report_name: str):
    """
    GET /api/reports/export/<report_name>
    Exports the requested report dataset to CSV using Pandas.
    """
    valid_reports = {
        "monthly_billing": lambda: ReportService.get_monthly_billing_summary(),
        "provider_utilization": lambda: ReportService.get_provider_utilization_report(),
        "outstanding_billing": lambda: ReportService.get_outstanding_billing_report().get("overdue_invoices", []),
    }

    if report_name not in valid_reports:
        raise ValidationException(
            f"Invalid export target '{report_name}'. Valid options: {list(valid_reports.keys())}"
        )

    records = valid_reports[report_name]()
    file_path = ReportService.export_report_to_csv(report_name, records)
    return send_file(file_path, as_attachment=True, download_name=f"{report_name}.csv", mimetype="text/csv")
