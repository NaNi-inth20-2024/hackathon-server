from datetime import datetime

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from tasks.models import Task, Grades
from tasks.serializers import GradesSerializer, TaskSerializer
from tasks.exceptions import TaskIsFinished, GradeIsPassed


class GradesView(viewsets.GenericViewSet):
    queryset = Grades.objects.all()
    serializer_class = GradesSerializer


class TaskView(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=["PUT"], name="Submit task")
    def submit(self, request, pk=None):
        task = self.get_object()
        user = request.user
        if task.is_finished:
            raise TaskIsFinished

        grade = Grades.objects.get(task=task, user=user)
        if grade.is_passed:
            raise GradeIsPassed

        grade.is_passed = True
        grade.save()
        return Response(GradesSerializer(grade).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["PUT"], name="Unsubmit task")
    def unsumbit(self, request, pk=None):
        task = self.get_object()
        user = request.user
        if task.is_finished:
            raise TaskIsFinished

        grade = Grades.objects.get(task=task, user=user)
        grade.is_passed = False
        grade.save()

        return Response(GradesSerializer(grade).data, status=status.HTTP_201_CREATED)
