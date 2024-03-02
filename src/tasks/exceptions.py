from rest_framework import status
from rest_framework.exceptions import APIException


class TaskIsFinished(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Task already is finished"


class GradeIsPassed(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Task already is passed"
