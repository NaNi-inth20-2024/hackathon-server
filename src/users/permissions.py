from rest_framework import permissions
from users.models import CustomUser


class IsStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            if user.role == CustomUser.Roles.STUDENT:
                return True
        return False


class IsSameStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            if user.role == CustomUser.Roles.STUDENT:
                if obj.id == user.id:
                    return True
        return False


class IsTeacher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            if user.role == CustomUser.Roles.TEACHER:
                return True
        return False


class IsStudentReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            user = request.user
            if user.is_authenticated:
                if user.role == CustomUser.Roles.STUDENT:
                    return True
        return False
