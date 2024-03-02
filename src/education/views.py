from rest_framework import viewsets
from education.models import Subject
from education.serializers import SubjectSerializer


class SubjectView(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer




