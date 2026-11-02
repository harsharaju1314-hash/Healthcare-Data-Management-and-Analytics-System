"""Routes Package"""
from app.routes.patients import patients_bp
from app.routes.appointments import appointments_bp
from app.routes.encounters import encounters_bp
from app.routes.billing import billing_bp
from app.routes.reports import reports_bp
from app.routes.dashboard import dashboard_bp
from app.routes.providers import providers_bp
from app.routes.system import system_bp

__all__ = [
    "patients_bp",
    "appointments_bp",
    "encounters_bp",
    "billing_bp",
    "reports_bp",
    "dashboard_bp",
    "providers_bp",
    "system_bp",
]
