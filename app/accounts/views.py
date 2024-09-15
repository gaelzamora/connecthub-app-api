"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions, viewsets, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from . import serializers

from accounts.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    ProjectSerializer,
    TechnologieSerializer
)

from core.models import Tag, WorkExperience, Project, Technologie

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authentication user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
    
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
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
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