"""File exceptions."""
from rest_framework.exceptions import APIException
from rest_framework import status


class NodeAlreadyExists(APIException):
    """File or directory already exists exception."""

    status_code = status.HTTP_409_CONFLICT
    default_detail = (
        "file or directory with this name already exists in the current directory."
    )
    default_code = "conflict"


class NodeNotFound(APIException):
    """File or directory doesn't exist exception."""

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = (
        "file or directory with this name does not exist in the current directory."
    )
    default_code = "not_found"


class InvalidPath(APIException):
    """Invalid path exception."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "incorrect path."
    default_code = "bad_request"
