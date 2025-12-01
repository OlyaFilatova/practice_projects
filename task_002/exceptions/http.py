class UserNotFound(Exception):
    """GitHub returned 404 response."""


class ConnectivityError(Exception):
    """Problem with connecting to the API."""
