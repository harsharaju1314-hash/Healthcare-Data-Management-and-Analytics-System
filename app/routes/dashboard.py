"""
Dashboard Analytics API Endpoints
"""

from flask import Blueprint
from app.services.report_service import ReportService
from app.utils.response import api_success

dashboard_bp = Blueprint("dashboard_api", __name__, url_prefix="/api/dashboard")


@dashboard_bp.route("/stats", methods=["GET"])
def get_dashboard_stats():
    """
    GET /api/dashboard/stats
    Returns aggregated high-level KPIs for dashboard cards.
    """
    stats = ReportService.get_dashboard_summary()
    return api_success(data=stats, message="Dashboard KPIs retrieved successfully")
