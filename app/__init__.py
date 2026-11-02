"""
Healthcare Application Factory Module
Configures Flask app, registers blueprints, and hooks global exception handlers.
"""

from flask import Flask, jsonify
from config import get_config
from app.utils.logger import logger
from app.utils.exceptions import HealthcareAppException
from app.utils.response import api_error
from app.routes.patients import patients_bp
from app.routes.appointments import appointments_bp
from app.routes.encounters import encounters_bp
from app.routes.billing import billing_bp
from app.routes.reports import reports_bp
from app.routes.dashboard import dashboard_bp
from app.routes.providers import providers_bp
from app.routes.system import system_bp


def create_app(config_object=None) -> Flask:
    """Creates and configures an instance of the Flask application."""
    app = Flask(__name__)

    # Apply configuration
    if config_object is None:
        config_object = get_config()
    app.config.from_object(config_object)

    # Register blueprints
    app.register_blueprint(system_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(encounters_bp)
    app.register_blueprint(billing_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(providers_bp)

    # Global Exception Handlers
    @app.errorhandler(HealthcareAppException)
    def handle_healthcare_exception(err: HealthcareAppException):
        """Catches custom domain and validation exceptions."""
        return api_error(
            message=err.message,
            status_code=err.status_code,
            details=err.details,
        )

    @app.errorhandler(404)
    def handle_not_found(err):
        """Catches 404 HTTP errors."""
        return api_error(message="Endpoint or resource not found", status_code=404)

    @app.errorhandler(500)
    def handle_server_error(err):
        """Catches unhandled server errors without leaking internals."""
        logger.error(f"Internal server error: {err}")
        return api_error(message="An internal server error occurred.", status_code=500)

    @app.after_request
    def set_security_headers(response):
        """Injects recommended security and cache headers."""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

    return app
