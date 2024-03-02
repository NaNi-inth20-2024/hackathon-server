from rest_framework import viewsets
from rest_framework.decorators import action

from education.models import Subject
from education.serializers import SubjectSerializer


class SubjectView(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    @action(detail=True, methods=["GET"], name="Submit task", url_path="tasks")
    def get_task(self):
        pass






