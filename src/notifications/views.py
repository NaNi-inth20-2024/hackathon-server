from django.shortcuts import render

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer, NotificationCreateForStudentSerializer, NotificationCreateForGroupSerializer
from users.permissions import IsTeacherOrReadOnly, IsTeacher
from users.models import CustomUser, Group


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]  # Allow listing for authenticated users

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(users=user, read=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        queryset.update(read=True)

        return Response(serializer.data)


class NotificationHistoryListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(users=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class NotificationCreateForGroupView(generics.CreateAPIView):
    serializer_class = NotificationCreateForGroupSerializer
    permission_classes = [IsTeacher]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            group_id = serializer.validated_data.get('group_id')
            group_students = CustomUser.objects.filter(group_id=group_id)
            for student in group_students:
                data = {'user': student.id, 'message': serializer.validated_data.get('message')}
                notification_serializer = NotificationSerializer(data=data)
                if notification_serializer.is_valid():
                    notification_serializer.save()
                else:
                    return Response(notification_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationCreateForUserView(generics.CreateAPIView):
    serializer_class = NotificationCreateForStudentSerializer
    permission_classes = [IsTeacher]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('user_id')
            message = serializer.validated_data.get('message')
            title = serializer.validated_data.get('title')
            user = CustomUser.objects.filter(pk=user_id).first()
            if user:
                notification = Notification.objects.create(user=user, title=title, message=message)
                return Response(NotificationSerializer(notification).data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
