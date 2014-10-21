"""
Exceptions for SmartyStreets requests.
"""

class SmartyStreetsError(Exception):
    """Unknown SmartyStreets error"""

    def __str__(self):
        return self.__doc__


class SmartyStreetsInputError(SmartyStreetsError):
    """HTTP 400 Bad input. Required fields missing from input or are malformed."""


class SmartyStreetsAuthError(SmartyStreetsError):
    """HTTP 401 Unauthorized. Authentication failure; invalid credentials"""


class SmartyStreetsPaymentError(SmartyStreetsError):
    """HTTP 422 Payment required. No active subscription found."""


class SmartyStreetsServerError(SmartyStreetsError):
    """HTTP 500 Internal server error. General service failure; retry request."""
