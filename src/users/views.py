from django.shortcuts import render
from rest_framework import viewsets, views, status
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from education.models import Group
from users.filters import StudentFilter
from users.serializers import StudentListSerializer, UserSerializer, UserAssignGroupSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from users.permissions import IsStudent, IsSameStudent, IsTeacher
from users.models import CustomUser


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

    def update(self, request, user_id: int, group_id: int):
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
    serializer_class = UserSerializer





