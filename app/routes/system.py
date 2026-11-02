"""
System Diagnostics and Web Views Blueprint
Serves HTML views for the interactive user interface and provides health checks.
"""

from flask import Blueprint, render_template, request
from app.repositories.db import db
from app.utils.response import api_success
from app.services.report_service import ReportService
from app.repositories.provider_repo import ProviderRepository
from app.repositories.patient_repo import PatientRepository

system_bp = Blueprint("system", __name__)


# -----------------------------------------------------------------------------
# REST Health Check Endpoint
# -----------------------------------------------------------------------------
@system_bp.route("/api/health", methods=["GET"])
def health_check():
    """
    GET /api/health
    Returns system status, active database engine, and connection health.
    """
    try:
        # Check database connectivity
        db.execute_one("SELECT 1 as ping")
        db_status = "connected"
    except Exception as e:
        db_status = f"unhealthy: {e}"

    return api_success(
        data={
            "status": "healthy" if "unhealthy" not in db_status else "degraded",
            "db_engine": db.engine,
            "is_oracle": db.is_oracle(),
            "database_status": db_status,
        },
        message="Healthcare API service is operational"
    )


# -----------------------------------------------------------------------------
# HTML Frontend User Interface Routes
# -----------------------------------------------------------------------------
@system_bp.route("/", methods=["GET"])
def view_dashboard():
    """Renders the main analytics dashboard."""
    kpis = ReportService.get_dashboard_summary()
    monthly_billing = ReportService.get_monthly_billing_summary()
    return render_template("dashboard.html", kpis=kpis, monthly_billing=monthly_billing)


@system_bp.route("/patients", methods=["GET"])
def view_patients():
    """Renders the patient management page."""
    search_q = request.args.get("search", "")
    patients = PatientRepository.search(search_q, limit=50)
    return render_template("patients.html", patients=patients, search=search_q)


@system_bp.route("/appointments", methods=["GET"])
def view_appointments():
    """Renders the appointment scheduling interface."""
    providers = ProviderRepository.get_all()
    return render_template("appointments.html", providers=providers)


@system_bp.route("/encounters", methods=["GET"])
def view_encounters():
    """Renders clinical encounters documentation view."""
    providers = ProviderRepository.get_all()
    return render_template("encounters.html", providers=providers)


@system_bp.route("/billing", methods=["GET"])
def view_billing():
    """Renders billing and invoice tracking view."""
    return render_template("billing.html")


@system_bp.route("/reports", methods=["GET"])
def view_reports():
    """Renders operational reports view."""
    providers = ProviderRepository.get_all()
    return render_template("reports.html", providers=providers)
