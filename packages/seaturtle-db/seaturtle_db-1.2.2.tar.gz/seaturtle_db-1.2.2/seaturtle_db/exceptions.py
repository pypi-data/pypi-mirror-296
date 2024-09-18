class NotFoundError(Exception):
    """Data that was specified to exist was not found."""

class DatabaseNotFoundError(NotFoundError):
    """The specified database directory was not found."""

class RecordNotFoundError(NotFoundError):
    """The specified record was not found."""

class RecordAlreadyExists(Exception):
    """The specified record already exists"""
