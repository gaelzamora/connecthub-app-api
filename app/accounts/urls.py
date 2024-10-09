"""
URL mapping for the user API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, WorkExperienceViewSet, ProjectViewSet, TechnologieViewSet, UploadImageUser

from . import views

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('work_experience', WorkExperienceViewSet)
router.register('project',  ProjectViewSet)
router.register('technologie', TechnologieViewSet)
router.register('upload_image', UploadImageUser)

app_name = 'accounts'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('<int:pk>/follow/', views.FollowUserView.as_view(), name='follow_user'),
    path('<int:pk>/unfollow/', views.UnfollowUserView.as_view(), name='unfollow_user'),
    path('search_user/', views.SearchUserViewSet.as_view(), name='search_user'),
    path('', include(router.urls)),
]
