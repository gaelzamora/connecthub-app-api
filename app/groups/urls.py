"""
URL mapping for the groups API.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet

from . import views

router = DefaultRouter()
router.register('', GroupViewSet)

app_name = 'groups'

urlpatterns = [
    path('', include(router.urls)),
    path('add_admin/<int:pk>/', views.AddAdminViewSet.as_view(), name='add_admin'),
    path('<int:pk>/posts/', views.GetPostAtGroupViewSet.as_view(), name='get_posts')
]
