from rest_framework import serializers
from tasks.models import Grades, Task
from users.views import CustomUser
from users.serializers import UserSerializer


class GradesSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Grades
        fields = ["id", "value", "is_passed", "user"]

    def create(self, validated_data):
        user = validated_data.pop("user")
        task = validated_data.pop("task")
        grade = Grades.objects.create(user=user, task=task, **validated_data)
        return grade


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["is_finished, subject"]

    def create(self, validated_data):
        subject = validated_data.pop("subject")
        task = Task.objects.create(subject=subject, **validated_data)
        return task
