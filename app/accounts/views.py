"""
Views for the user API.
"""
from rest_framework import status, generics, authentication, permissions, viewsets, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from . import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.decorators import action

from accounts import serializers

from core.models import Tag, WorkExperience, Project, Technologie, User
from .serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authentication user."""
    serializer_class = serializers.UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
    
class UploadImageUser(viewsets.ModelViewSet):
    """Upload image to unique user."""
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        """Retrieve user information for authenticated user."""    
        return self.queryset.filter(pk=request.user.pk)
    
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'upload_image':
            return serializers.UserImageSerializer
        
        return self.serializer_class
    

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request):
        """Upload an image to user."""
        user = request.user
        serializer = self.get_serializer(user, data=request.data)

        print(serializer)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowUserView(APIView):
    """Allow the authenticated user to follow another user"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        """Handle follow action"""
        try:
            user_to_follow = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if user_to_follow == request.user:
            return Response({"detail": "You can't follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.follows.add(user_to_follow)
        return Response({"detail": f"Now you follow {user_to_follow.get_full_name()}."}, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    """Allow the authenticated user to unfollow another user"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        """Handle unfollow action"""
        try:
            user_to_unfollow = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if user_to_unfollow == request.user:
            return Response({"detail": "You can't unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.follows.remove(user_to_unfollow)
        return Response({"detail": f"Now you unfollow {user_to_unfollow.get_full_name()}."}, status=status.HTTP_200_OK)

class TagViewSet(
        mixins.CreateModelMixin, 
        mixins.DestroyModelMixin, 
        mixins.UpdateModelMixin, 
        mixins.ListModelMixin, 
        viewsets.GenericViewSet
    ):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new tag and assign it to the authenticated user."""
        serializer.save(user=self.request.user)

class WorkExperienceViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Manage work experiences in the database."""
    serializer_class = serializers.WorkExperienceSerializer
    queryset = WorkExperience.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-time')
    
    def perform_create(self, serializer):
        """Create a new work experience it to the authenticated user."""
        serializer.save(user=self.request.user)

class ProjectViewSet(
    viewsets.ModelViewSet
):
    """Manage projects in the database."""
    serializer_class = serializers.ProjectSerializer
    queryset = Project.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-year')
    
    def perform_create(self, serializer):
        """Create a new project it to the authenticated user."""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ProjectSerializer
        
        return self.serializer_class

class TechnologieViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Manage technologies in the database."""
    serializer_class = serializers.TechnologieSerializer
    queryset = Technologie.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SearchUserViewSet(APIView):
    """Allow the authenticated user can search to user."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('query')
        if query is None:
            query = ''

        user = User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))

        serializer = UserSerializer(user, many=True)

        return Response({'users': serializer.data})