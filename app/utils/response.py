"""
API Response Formatting Utility
Standardizes JSON responses and pagination across all endpoints.
"""

from decimal import Decimal
from datetime import date, datetime
from flask import jsonify, Response


def serialize_item(item):
    """Recursively converts Decimals, Dates, and Datetimes to JSON-safe representations."""
    if isinstance(item, dict):
        return {k: serialize_item(v) for k, v in item.items()}
    elif isinstance(item, list):
        return [serialize_item(x) for x in item]
    elif isinstance(item, Decimal):
        return float(item)
    elif isinstance(item, (datetime, date)):
        return item.isoformat()
    return item


def api_success(data=None, message: str = "Operation successful", status_code: int = 200, meta: dict = None) -> Response:
    """Returns a standardized success JSON response."""
    payload = {
        "success": True,
        "message": message,
        "data": serialize_item(data) if data is not None else None,
    }
    if meta is not None:
        payload["meta"] = meta

    response = jsonify(payload)
    response.status_code = status_code
    return response


def api_error(message: str, status_code: int = 400, details: dict = None) -> Response:
    """Returns a standardized error JSON response without leaking database internals."""
    payload = {
        "success": False,
        "error": message,
        "details": details or {},
    }
    response = jsonify(payload)
    response.status_code = status_code
    return response


def api_paginated(items: list, total: int, page: int, page_size: int, message: str = "Records retrieved") -> Response:
    """Returns a standardized paginated JSON response."""
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 1
    meta = {
        "page": page,
        "page_size": page_size,
        "total_records": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
    return api_success(data=items, message=message, meta=meta)
