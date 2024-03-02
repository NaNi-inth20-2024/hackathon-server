from rest_framework import serializers
from users.models import CustomUser
from education.serializers import GroupSerializer


class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name", "group"]
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
