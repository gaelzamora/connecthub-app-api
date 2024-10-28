from django.urls import path
from .views import NotificationListView, CreateNotificationView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notifications-list'),
    path('notifications/create/', CreateNotificationView.as_view(), name='create-notification'),
]
