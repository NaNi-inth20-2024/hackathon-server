from rest_framework import status
from rest_framework.exceptions import APIException


class TaskIsFinished(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Task already is finished"

class TaskIsGraded(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Task already is graded"


class GradeIsPassed(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Task already is passed"


class TaskIsNotPassed(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Status is not passed"


class GradeIncorrect(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Grade is incorrect. Check nax possible grade for this task"
