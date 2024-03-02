from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from education.models import Group, Subject

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        STUDENT = "STUDENT", _("Student")
        TEACHER = "TEACHER", _("Teacher")

    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(null=True)
    last_name = models.CharField(null=True)
    age = models.PositiveIntegerField(null=True, default=20)
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    subjects = models.ManyToManyField(Subject)

    objects = CustomUserManager()

    role = models.CharField(choices=Roles.choices, default=Roles.TEACHER)

    def __str__(self):
        return self.email
