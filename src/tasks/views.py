from datetime import datetime

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from users.permissions import IsStudentReadOnly, IsTeacher, IsStudent
from tasks.models import Task, Grades
from tasks.serializers import GradesSerializer, TaskSerializer
from tasks.exceptions import TaskIsFinished, GradeIsPassed, TaskIsGraded, TaskIsNotPassed, GradeIncorrect
from users.views import CustomUser


class GradesView(viewsets.GenericViewSet):
    queryset = Grades.objects.all()
    serializer_class = GradesSerializer
    permission_classes = [IsTeacher]

    @action(detail=True, methods=["POST"], name="Set grade to task", url_path="value/(?P<grade_val>[^/.]+)")
    def set_value(self, request, pk=None, grade_val: int = None):
        grade = self.get_object()
        grade_val = int(grade_val)
        print(1)

        if not grade.is_passed:
            raise TaskIsNotPassed

        if grade_val > grade.task.max_points or grade_val < 1:
            raise GradeIncorrect
        print(2)
        grade.value = grade_val
        grade.save()

        return Response(GradesSerializer(grade).data)


class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsTeacher | IsStudent]

    def retrieve(self, request, pk=None):
        user = request.user
        task = self.get_object()

        serializer = self.get_serializer(task)
        data = serializer.data
        if user.role == CustomUser.Roles.TEACHER:
            grades = Grades.objects.filter(is_passed=True, task=task)
        else:
            grades = Grades.objects.filter(user=user, task=task)

        grade = GradesSerializer(grades, many=True).data
        if grade:
            data["grade"] = grade
        return Response(data)

    @action(detail=True, methods=["PUT"], name="Submit task", permission_classes=[IsStudent])
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

    @action(detail=True, methods=["PUT"], name="Unsubmit task", permission_classes=[IsStudent])
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
