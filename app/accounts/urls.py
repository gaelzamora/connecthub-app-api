"""
URL mapping for the user API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, WorkExperienceViewSet, ProjectViewSet, TechnologieViewSet, LoginView
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('work_experience', WorkExperienceViewSet)
router.register('project',  ProjectViewSet)
router.register('technologie', TechnologieViewSet)

app_name = 'accounts'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('user-info/', views.UserDetailView.as_view(), name='user-info'),
    path('login/', views.LoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('<int:pk>/follow/', views.FollowUserView.as_view(), name='follow_user'),
    path('<int:pk>/unfollow/', views.UnfollowUserView.as_view(), name='unfollow_user'),
    path('search_user/', views.SearchUserViewSet.as_view(), name='search_user'),
    path('upload_image/', views.UploadImageUserViewSet.as_view(), name='upload_image'),
    path('', include(router.urls)),
]
