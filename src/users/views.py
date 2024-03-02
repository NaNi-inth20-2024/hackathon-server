from django.shortcuts import render
from rest_framework import viewsets, views
from users.serializers import StudentListSerializer, UserSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser


class StudentListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = StudentListSerializer
    permission_classes = IsAuthenticated


class UserView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
