'''
Views for logical of Posts.
'''

from rest_framework.views import APIView
from rest_framework import mixins, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import PostSerializer
from core.models import Post

class PostViewSet(
    viewsets.GenericViewSet, 
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin
):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-posted')
    
    def perform_create(self, serializer):
        print(serializer)
        serializer.save(autor=self.request.user)

class LikeActionView(APIView):
    """Allow the authenticated user to like post."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.post.likes.contains(request.user):
            request.post.likes.remove(request.user)
            return Response({"detail": f"Now, you don't liked this post {post.content}."})

        request.post.likes.add(request.user)
        return Response({"detail": f"Now, you like this post {post.content}."})