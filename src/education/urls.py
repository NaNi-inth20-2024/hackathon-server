from django.urls import path, include
from rest_framework.routers import DefaultRouter

from education.views import SubjectView, GroupView

router = DefaultRouter()
router.register(r"subjects", SubjectView, basename="subject")
router.register(r"groups", GroupView, basename="groups")

urlpatterns = [

] + router.urls
