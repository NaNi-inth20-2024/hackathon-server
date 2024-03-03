from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserView, StudentListView, StudentUpdateView, StudentDestroyView, StudentRetrieveView, StudentUpdateGroupView, TeacherListRetrieveView

router = DefaultRouter()
router.register(r"users", UserView, basename="user")

urlpatterns = [
    path(r"students/", StudentListView.as_view(), name="student-list"),
    path(r"students/<int:pk>", StudentRetrieveView.as_view(), name="student-retrieve"),
    path(r"students/", StudentUpdateView.as_view(), name="student-update"),
    path(r"students/<int:pk>", StudentDestroyView.as_view(), name="student-destroy"),
    path(r"students/<int:user_id>/assign_group/", StudentUpdateGroupView.as_view(), name="student-group_assign"),
    path(r"teachers/", TeacherListRetrieveView.as_view(), name="teacher-get"),
] + router.urls
