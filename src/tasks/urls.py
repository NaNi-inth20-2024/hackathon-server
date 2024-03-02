from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tasks.views import TaskView, GradesView

router = DefaultRouter()
router.register(r"tasks", TaskView, basename="task")
router.register(r"grades", GradesView, basename="grade")

urlpatterns = [
    path("", include(router.urls)),
]