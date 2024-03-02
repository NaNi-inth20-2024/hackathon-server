from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserView, StudentListView

router = DefaultRouter()
router.register(r"", UserView, basename="user")

urlpatterns = [
    path(r"students/", StudentListView.as_view(), name="student-list")
] + router.urls
