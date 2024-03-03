from django.core.validators import MaxValueValidator
from django.db import models
from users.models import CustomUser
from education.models import Subject

MAX_TITLE_LEN = 1024
MAX_DESC_NAME = 4096
MAX_GRADE = 200


class Task(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    title = models.CharField(max_length=MAX_TITLE_LEN)
    description = models.CharField(max_length=MAX_DESC_NAME)
    is_finished = models.BooleanField(default=False)
    max_points = models.PositiveIntegerField()


class Grades(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # TODO
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    value = models.IntegerField(validators=[MaxValueValidator(MAX_GRADE)])
    is_passed = models.BooleanField(default=False)