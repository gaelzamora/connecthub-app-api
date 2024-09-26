'''
Views for logical of Posts.
'''

from rest_framework.views import APIView
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from serializers import PostSerializer
from accounts import Post

class PostViewSet(
    viewsets.GenericViewSet, 
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin
):
    serializer_class = PostSerializer
    queryset = Post
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-posted')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)