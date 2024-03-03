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

    @action(detail=True, methods=["GET"], name="Get all statistic of user")
    def statistic(self, request, pk=None):
        user = self.get_object()
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
                        koef.append(grade.value / max)
                else:
                    active_subject_tasks += 1

            if completed_subject_tasks == active_subject_tasks:
                completed_subjects += 1
            else:
                unfinished_subjects += 1
            completed_tasks += completed_subject_tasks
            active_tasks += active_subject_tasks

        data = {
            "average_grade": (sum(koef) / len(koef)) * 100,
            "completed_tasks": completed_tasks,
            "active_tasks": active_tasks,
            "completed_tasks_ratio": completed_tasks / (completed_tasks + active_tasks),
            "completed_subjects": completed_subjects,
            "unfinished_subjects": unfinished_subjects,
            "completed_subject_ration": completed_subjects / (completed_subjects + unfinished_subjects)
        }
        return Response(data=data, status=status.HTTP_200_OK)
