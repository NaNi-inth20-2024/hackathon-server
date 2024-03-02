from django.urls import path, include
from rest_framework.routers import DefaultRouter

from education.views import SubjectView

router = DefaultRouter()
router.register(r"subjects", SubjectView, basename="subject")

urlpatterns = [
    path("", include(router.urls)),
]