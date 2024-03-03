from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class NotificationCreateForGroupSerializer(serializers.ModelSerializer):
    group_id = serializers.IntegerField()

    class Meta:
        model = Notification
        fields = ['group_id', 'title', 'message']


class NotificationCreateForStudentSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField()

    class Meta:
        model = Notification
        fields = ['user_id', 'title', 'message']

