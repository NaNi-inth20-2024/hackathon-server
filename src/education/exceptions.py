from rest_framework import status
from rest_framework.exceptions import APIException


class SubjectInvalidException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Subject is not valid"
