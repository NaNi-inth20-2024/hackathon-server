from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from education.exceptions import SubjectInvalidException
from education.models import Subject, Group
from education.serializers import SubjectSerializer, GroupSerializer
from services.education import is_subject_valid
from users.models import CustomUser
from tasks.models import Task, Grades
from tasks.serializers import TaskSerializer, GradesSerializer
from users.permissions import IsStudentReadOnly, IsTeacher
from users.serializers import UserSerializer


class SubjectView(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsStudentReadOnly | IsTeacher]

    def list(self, request, *args, **kwargs):
        user = request.user
        subjects = user.subjects.all()
        subject_teachers = []
        for subject in subjects:
            teachers = CustomUser.objects.filter(subjects=subject, role=CustomUser.Roles.TEACHER)
            teachers = UserSerializer(teachers, many=True).data
            subject_teachers.append(teachers)

        serializer = self.get_serializer(subjects, many=True)

        data = serializer.data
        for subject_data in data:
            subject_data["teachers"] = subject_teachers.pop()

        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        subject = self.get_object()
        serializer = self.get_serializer(subject)
        data = serializer.data
        teachers = CustomUser.objects.filter(subjects=subject, role=CustomUser.Roles.TEACHER)
        teachers = UserSerializer(teachers, many=True).data
        data["teachers"] = teachers
        return Response(data)

    def create(self, request, *args, **kwargs):
        teacher = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject = serializer.save()
        teacher.subjects.add(subject)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"], name="Get tasks", url_path="tasks")
    def get_tasks(self, request, pk=None):
        subject = self.get_object()
        user = request.user
        tasks = Task.objects.filter(subject=subject)
        serialized_tasks = []

        if not user.is_authenticated:
            serialized_tasks = TaskSerializer(tasks, many=True).data
            return Response(serialized_tasks)

        for task in tasks:
            if user.role == CustomUser.Roles.TEACHER:
                grade = Grades.objects.filter(is_passed=True, task=task)
            else:
                grade = Grades.objects.filter(task=task, user=user)
            if not grade:
                continue
            grade = GradesSerializer(grade, many=True).data
            serialized_task = TaskSerializer(task).data
            serialized_task["grade"] = grade
            serialized_tasks.append(serialized_task)
        return Response(serialized_tasks)

    @action(detail=True, methods=["GET"], name="Get users of subject", url_path="users")
    def subject_tasks(self, request, pk=None):
        subject = self.get_object()
        users = CustomUser.objects.filter(subjects=subject)
        users = UserSerializer(users, many=True).data
        return Response(users)

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
            if user.role != CustomUser.Roles.TEACHER:
                Grades(user=user, task=task, value=0).save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=["PUT"], name="Add new user to subject", url_path="users/(?P<user_id>[^/.]+)")
    def add_user(self, request, pk=None, user_id=None):
        subject = self.get_object()
        user = CustomUser.objects.get(pk=user_id)
        user.subjects.add(subject)

        if not is_subject_valid(subject):
            raise SubjectInvalidException

        tasks = Task.objects.filter(subject=subject)
        for task in tasks:
            if user.role != CustomUser.Roles.TEACHER:
                Grades(user=user, task=task, value=0).save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class GroupView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsStudentReadOnly, IsTeacher]
