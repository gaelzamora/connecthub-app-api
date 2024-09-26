'''
URL mapping for the posts API.
'''

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register('', PostViewSet)

app_name = 'posts'

urlpatterns = [
    path('', include(router.urls))
]
