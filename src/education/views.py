from rest_framework import viewsets
from rest_framework.decorators import action

from education.models import Subject, Group, Discipline
from education.serializers import SubjectSerializer, GroupSerializer, DisciplineSerializer


class SubjectView(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    @action(detail=True, methods=["GET"], name="Get tasks", url_path="tasks")
    def get_task(self):
        pass


class GroupView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class DisciplineView(viewsets.ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer
