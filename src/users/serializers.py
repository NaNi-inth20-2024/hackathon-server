from rest_framework import serializers
from users.models import CustomUser


class StudentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "second_name", "group"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
