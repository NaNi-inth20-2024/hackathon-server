from datetime import datetime

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from tasks.models import Task, Grades
from tasks.serializers import GradesSerializer, TaskSerializer
from tasks.exceptions import TaskIsFinished, GradeIsPassed, TaskIsGraded, TaskIsNotPassed, GradeIncorrect


class GradesView(viewsets.GenericViewSet):
    queryset = Grades.objects.all()
    serializer_class = GradesSerializer


class TaskView(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=["PUT"], name="Set grade to task", url_path="grade/(?P<value>[^/.]+)")
    def set_grade(self, pk=None, value=None):
        task = self.get_object()
        grade = Grades.objects.get(task=task)

        if not grade.is_passed:
            raise TaskIsNotPassed

        if value > task.max_points:
            raise GradeIncorrect

        grade.value = value
        grade.save()
        return Response(GradesSerializer(grade).data)

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
        if grade.value != 0:
            raise TaskIsGraded

        grade.is_passed = False
        grade.save()

        return Response(GradesSerializer(grade).data, status=status.HTTP_201_CREATED)
