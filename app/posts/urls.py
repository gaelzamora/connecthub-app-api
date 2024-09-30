'''
URL mapping for the posts API.
'''

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

from . import views

router = DefaultRouter()
router.register('', PostViewSet)

app_name = 'posts'

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/like/', views.LikeActionView.as_view(), name='like_user'),
    path('post/<int:pk>/', views.GetPostView.as_view(), name='post_user'),
    path('create_hashtag/<int:pk>/', views.CreateHashtagView.as_view(), name='hashtag_post')
]