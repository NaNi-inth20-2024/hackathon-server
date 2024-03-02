from rest_framework import serializers
from education.models import Subject, Group, Discipline


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = "__all__"
