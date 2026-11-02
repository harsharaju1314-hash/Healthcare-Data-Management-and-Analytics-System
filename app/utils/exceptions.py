"""
Custom Application Exceptions
Defines standard exceptions for healthcare business workflows and database access.
"""


class HealthcareAppException(Exception):
    """Base exception for all application errors."""
    def __init__(self, message: str, status_code: int = 500, details=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}


class ResourceNotFoundException(HealthcareAppException):
    """Raised when an entity (patient, appointment, bill) is not found."""
    def __init__(self, message: str = "Resource not found", details=None):
        super().__init__(message, status_code=404, details=details)


class ValidationException(HealthcareAppException):
    """Raised when client input or business payload fails validation."""
    def __init__(self, message: str = "Validation failed", details=None):
        super().__init__(message, status_code=400, details=details)


class ConflictException(HealthcareAppException):
    """Raised when an operation conflicts with existing state (e.g. appointment collision, duplicate MRN)."""
    def __init__(self, message: str = "Resource conflict detected", details=None):
        super().__init__(message, status_code=409, details=details)


class DatabaseException(HealthcareAppException):
    """Raised when an underlying database query or transaction fails."""
    def __init__(self, message: str = "Database operation failed", details=None):
        super().__init__(message, status_code=500, details=details)
