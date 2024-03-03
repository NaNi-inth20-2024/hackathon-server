from django.db import models
from users.models import CustomUser

MAX_MESSAGE_SIZE = 2046
MAX_TITLE_SIZE = 100


class Notification(models.Model):
    users = models.ManyToManyField(CustomUser, related_name='notifications')
    title = models.CharField(max_length=MAX_TITLE_SIZE)
    message = models.TextField(max_length=MAX_MESSAGE_SIZE)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
