from django.shortcuts import render
from rest_framework import viewsets, views
from rest_framework.filters import SearchFilter, OrderingFilter
from users.filters import StudentFilter
from users.serializers import StudentListSerializer, UserSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from users.models import CustomUser


class StudentListView(ListAPIView):
    queryset = CustomUser.objects.all()
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


class UserView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer



