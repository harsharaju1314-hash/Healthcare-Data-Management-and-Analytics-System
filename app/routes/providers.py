"""
Healthcare Provider REST API Endpoints
"""

from flask import Blueprint, request
from app.repositories.provider_repo import ProviderRepository
from app.utils.response import api_success
from app.utils.exceptions import ResourceNotFoundException

providers_bp = Blueprint("providers", __name__, url_prefix="/api/providers")


@providers_bp.route("", methods=["GET"])
def get_providers():
    """
    GET /api/providers
    Retrieves all providers with optional department filtering.
    """
    dept = request.args.get("department")
    if dept:
        providers = ProviderRepository.get_by_department(dept)
    else:
        providers = ProviderRepository.get_all()
    return api_success(data=providers, message="Providers retrieved successfully")


@providers_bp.route("/<int:provider_id>", methods=["GET"])
def get_provider(provider_id: int):
    """
    GET /api/providers/<provider_id>
    Retrieves a single provider by ID.
    """
    prov = ProviderRepository.get_by_id(provider_id)
    if not prov:
        raise ResourceNotFoundException(f"Provider ID {provider_id} not found.")
    return api_success(data=prov, message="Provider retrieved successfully")
