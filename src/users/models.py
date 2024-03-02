from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from education.models import Group

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        STUDENT = "STUDENT", _("Student")
        TEACHER = "TEACHER", _("Teacher")

    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField()
    second_name = models.CharField()
    age = models.PositiveIntegerField()
    group = models.OneToOneField(Group, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    role = models.CharField(choices=Roles.choices, default=Roles.TEACHER)

    def __str__(self):
        return self.email
