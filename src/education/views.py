from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from education.exceptions import SubjectInvalidException
from education.models import Subject, Group, Discipline
from education.serializers import SubjectSerializer, GroupSerializer, DisciplineSerializer
from services.education import is_subject_valid
from users.models import CustomUser
from tasks.models import Task, Grades
from tasks.serializers import TaskSerializer, GradesSerializer
from users.serializers import UserSerializer


class SubjectView(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    @action(detail=True, methods=["GET"], name="Get tasks", url_path="tasks")
    def get_tasks(self, request, pk=None):
        subject = self.get_object()
        tasks = Task.objects.filter(subject=subject)
        serialized_tasks = []

        if not request.user.is_authenticated:
            serialized_tasks = TaskSerializer(tasks, many=True).data
            return Response(serialized_tasks)

        for task in tasks:
            grade = Grades.objects.filter(task=task, user=request.user)
            if not grade:
                continue
            grade = GradesSerializer(grade[0]).data
            serialized_task = TaskSerializer(task).data
            serialized_task["grade"] = grade
            serialized_tasks.append(serialized_task)
        return Response(serialized_tasks)

    @action(detail=True, methods=["POST"], name="Create task", url_path="addtask")
    def add_task(self, request, pk=None):
        subject = self.get_object()
        task = request.data
        task["subject"] = pk
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()

        if not is_subject_valid(subject):
            raise SubjectInvalidException

        users = CustomUser.objects.filter(subjects__id=subject.id)

        for user in users:
            Grades(user=user, task=task, value=0).save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=["PUT"], name="Add student", url_path="student/(?P<student_id>[^/.]+)")
    def add_student(self, request, pk=None, student_id=None):
        subject = self.get_object()
        student = CustomUser.objects.get(pk=student_id)
        student.subjects.add(subject)

        if not is_subject_valid(subject):
            raise SubjectInvalidException

        tasks = Task.objects.filter(subject=subject)
        for task in tasks:
            Grades(user=student, task=task, value=0).save()
        return Response(UserSerializer(student).data, status=status.HTTP_200_OK)


class GroupView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class DisciplineView(viewsets.ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer
