from django.shortcuts import render
from rest_framework import viewsets, views, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response

import education.models
import tasks.models
from education.models import Group
from users.filters import StudentFilter
from users.serializers import StudentListSerializer, UserAssignGroupSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from users.permissions import IsStudent, IsSameStudent, IsTeacher
from users.models import CustomUser


# from education.models import Subject
# from education.serializers import SubjectSerializer
# from tasks.models import Task, Grades
# from tasks.serializers import TaskSerializer, GradesSerializer


class StudentListView(ListAPIView):
    queryset = CustomUser.objects.filter(role__exact=CustomUser.Roles.STUDENT)
    serializer_class = StudentListSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = [
        "first_name",
        "last_name",
        "group",
    ]
    search_fields = [
        "first_name",
        "last_name",
        "group__name",
    ]
    filterset_class = StudentFilter


class StudentRetrieveView(RetrieveAPIView):
    queryset = CustomUser.objects.filter(role__exact=CustomUser.Roles.STUDENT)
    serializer_class = StudentListSerializer
    permission_classes = [IsAuthenticated]


class StudentUpdateView(UpdateAPIView):
    queryset = CustomUser.objects.filter(role__exact=CustomUser.Roles.STUDENT)
    serializer_class = StudentListSerializer
    permission_classes = [IsSameStudent]


class StudentUpdateGroupView(UpdateAPIView):
    queryset = CustomUser.objects.filter(role__exact=CustomUser.Roles.STUDENT)
    serializer_class = UserAssignGroupSerializer
    permission_classes = [IsTeacher]

    def update(self, request, user_id: int):
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            raise NotFound(detail="User not found", code=status.HTTP_404_NOT_FOUND)

        serializer = UserAssignGroupSerializer(data=request.data)
        if serializer.is_valid():
            group_id = serializer.validated_data.get('group_id')
            try:
                group = Group.objects.get(pk=group_id)
            except Group.DoesNotExist:
                raise NotFound(detail="Group not found", code=status.HTTP_404_NOT_FOUND)

            user.group = group
            user.save()
            return Response({'message': 'User group assigned successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDestroyView(DestroyAPIView):
    queryset = CustomUser.objects.filter(role__exact=CustomUser.Roles.STUDENT)
    serializer_class = StudentListSerializer
    permission_classes = [IsTeacher]


class TeacherListRetrieveView(GenericAPIView, ListModelMixin, RetrieveModelMixin):
    queryset = CustomUser.objects.filter(role__exact=CustomUser.Roles.TEACHER)
    serializer_class = StudentListSerializer
    permission_classes = [IsAuthenticated]


class UserView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = IsStudent | IsTeacher

    @action(detail=False, methods=["GET"], name="Get all grades of user relative to subjects",
            permission_classes=[IsStudent])
    def grades(self, request):
        user = request.user
        subjects = education.models.Subject.objects.filter(customuser=user)
        res_data = []
        for subject in subjects:
            data = education.serializers.SubjectSerializer(subject).data
            task_arr = tasks.models.Task.objects.filter(subject=subject)
            subject_grade = 0
            max_subject_grade = 0
            for task in task_arr:
                max_subject_grade += task.max_points
                grade = tasks.models.Grades.objects.filter(task=task)
                if not grade:
                    continue
                if grade[0] != 0:
                    subject_grade += grade[0].value

            data["grade"] = {
                "max": max_subject_grade,
                "my": subject_grade,
            }
            res_data.append(data)
        return Response(data=res_data)

    @action(detail=False, methods=["GET"], name="Get all statistic of user", permission_classes=[IsStudent])
    def statistic(self, request):
        user = request.user
        subjects = education.models.Subject.objects.filter(customuser=user)
        koef = []
        completed_tasks = 0
        active_tasks = 0
        completed_subjects = 0
        unfinished_subjects = 0
        for subject in subjects:
            completed_subject_tasks = 0
            active_subject_tasks = 0
            task_arr = tasks.models.Task.objects.filter(subject=subject)
            for task in task_arr:
                max = task.max_points
                grade = tasks.models.Grades.objects.filter(task=task)
                if not grade:
                    continue
                grade = grade[0]
                if grade.is_passed:
                    completed_subject_tasks += 1
                    if grade.value != 0:
                        if max != 0:
                            koef.append(grade.value / max)
                else:
                    active_subject_tasks += 1

            if completed_subject_tasks == active_subject_tasks:
                completed_subjects += 1
            else:
                unfinished_subjects += 1
            completed_tasks += completed_subject_tasks
            active_tasks += active_subject_tasks
        try:
            average_grade = (sum(koef) / len(koef)) * 100,
        except ZeroDivisionError:
            average_grade = 0
        try:
            completed_tasks_ratio = completed_tasks / (completed_tasks + active_tasks),
        except ZeroDivisionError:
            completed_tasks_ratio = 0
        try:
            completed_subject_ratio = completed_subjects / (completed_subjects + unfinished_subjects)
        except ZeroDivisionError:
            completed_subject_ratio = 0

        data = {
            "average_grade": average_grade,
            "completed_tasks": completed_tasks,
            "active_tasks": active_tasks,
            "completed_tasks_ratio": completed_tasks_ratio,
            "completed_subjects": completed_subjects,
            "unfinished_subjects": unfinished_subjects,
            "completed_subject_ratio": completed_subject_ratio
        }
        return Response(data=data, status=status.HTTP_200_OK)
