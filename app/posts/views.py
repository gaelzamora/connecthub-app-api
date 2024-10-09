'''
Views for logical of Posts.
'''

from rest_framework.views import APIView
from rest_framework import mixins, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import PostSerializer
from core.models import Group, Post, Hashtag

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
        return self.queryset.filter(author=self.request.user).order_by('-posted')
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class LikeActionView(APIView):
    """Allow the authenticated user to like post."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        if post.likes.filter(id=request.user.pk).exists():
            post.likes.remove(request.user)
            return Response({"detail": f"Now you don't like this post {post.content}"})

        post.likes.add(request.user)
        post.save()
        return Response({"detail": f"Now, you like this post {post.content}"})
    
class GetPostView(APIView):
    """Get a post with a pk."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status.HTTP_400_BAD_REQUEST)
        
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data)
    
class CreateHashtagView(APIView):
    """Create a hashtag when there a post created."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status.HTTP_400_BAD_REQUEST)
        hashtag = Hashtag.objects.create(
            name=request.data['name'],
            user=request.user
        ) 

        post.hashtags.add(hashtag)
        return Response({"detail": "It've created a new hashtag."})
    