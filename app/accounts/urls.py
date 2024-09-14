"""
URL mapping for the user API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, WorkExperienceViewSet, ProjectViewSet, TechnologieViewSet

from . import views

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('work_experience', WorkExperienceViewSet)
router.register('project',  ProjectViewSet)
router.register('technologie', TechnologieViewSet)

app_name = 'accounts'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('', include(router.urls)),
]
