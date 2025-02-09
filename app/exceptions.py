class PatientNotFoundException(Exception):
    """Raised when a patient record cannot be found."""
    pass

class InvalidRequestException(Exception):
    """Raised when a request is invalid due to missing or malformed data."""
    pass

class DatabaseIntegrityError(Exception):
    """Raised when a database operation violates integrity constraints."""
    pass

class InternalServerError(Exception):
    """Raised for unexpected server-side errors."""
    pass
class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass
class PatientDeletionError(Exception):
    """Raised when there's an error deleting a patient record."""
    pass
class ReplicationError(Exception):
    """Raised when there's an error in data replication."""
    pass
class PatientNotFoundError(Exception):
    pass