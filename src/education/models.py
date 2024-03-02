from datetime import timezone

from django.db import models
from users.models import CustomUser
from django.core.validators import MaxValueValidator

DISCIPLINE_NAME_MAX_SIZE = 150
GROUP_NAME_MAX_SIZE = 10
MAX_YEAR = 3000


class Discipline(models.Model):
    name = models.CharField(max_length=DISCIPLINE_NAME_MAX_SIZE)


class Subject(models.Model):
    SEMESTER_CHOICES = (
        (1, 'Semester 1'),
        (2, 'Semester 2'),
    )

    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES)
    name = models.CharField(max_length=DISCIPLINE_NAME_MAX_SIZE)
    discipline = models.ForeignKey(Discipline)
    year = models.PositiveIntegerField([MaxValueValidator(MAX_YEAR)])
    users = models.ManyToManyField(CustomUser, null=True)


class Group(models.Model):
    name = models.CharField(max_length=GROUP_NAME_MAX_SIZE)
    year = models.PositiveIntegerField(validators=[MaxValueValidator(MAX_YEAR)])
