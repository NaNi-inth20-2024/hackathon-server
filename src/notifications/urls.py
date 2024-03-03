from django.urls import path
from .views import NotificationListView, NotificationCreateForUserView, NotificationCreateForGroupView, NotificationHistoryListView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/history/', NotificationHistoryListView.as_view(), name='notification-history'),
    path('notifications/create/group/', NotificationCreateForGroupView.as_view(), name='notification-group-create'),
    path('notifications/create/student', NotificationCreateForUserView.as_view(), name='notification-user-create')
]