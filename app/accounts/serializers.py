"""
Serializers for the user API VIEW.
"""

from django.contrib.auth import (
    get_user_model,
    authenticate
)
from django.utils.translation import gettext as _

from core.models import Tag, WorkExperience, Project, Technologie

from rest_framework import serializers

from rest_framework.authtoken.models import Token


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class WorkExperienceSerializer(serializers.ModelSerializer):
    """Serializer for work experiences."""

    class Meta:
        model = WorkExperience
        fields = ['id', 'business', 'time', 'current_job', 'position', 'description']
        read_only_fields = ['id']

class TechnologieSerializer(serializers.ModelSerializer):
    """Serializer for technologies."""

    class Meta:
        model = Technologie
        fields = ['id', 'name']
        read_only_fields = ['id']

class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for projects"""
    technologies = TechnologieSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'technologies', 'year']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create and return a project."""
        technologies = validated_data.pop('project_technologies', [])
        project = Project.objects.create(**validated_data)
        self._get_or_create_technologies(technologies, project)
        return project

    def _get_or_create_technologies(self, technologies_data, project):
        """Helper method to create or get technologies and assign them to the project."""
        technologie_objects = []
        for technologie_data in technologies_data:
            technologie_obj, created = Technologie.objects.get_or_create(**technologie_data)
            technologie_objects.append(technologie_obj)
        project.technologies.set(technologie_objects)

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""
    tags = TagSerializer(many=True, source='user_tags', required=False)
    work_experiences = WorkExperienceSerializer(many=True, source='user_experience', required=False)
    projects = ProjectSerializer(many=True, source='user_project', required=False)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'first_name', 'last_name', 'tags', 'work_experiences', 'projects']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encripted password."""
        tags = validated_data.pop('user_tags', [])
        work_experiences = validated_data.pop('user_experience', [])
        projects = validated_data.pop('user_project', [])
        user = get_user_model().objects.create_user(**validated_data)
        self._get_or_create_tags(tags, user)
        self._get_or_create_experiences(work_experiences, user)
        self._get_or_create_projects(projects, user)
        return user

    def update(self, instance, validated_data):
        """Update and return user."""
        tags = validated_data.pop('user_tags', None)
        work_experiences = validated_data.pop('user_experience', None)
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        if tags: self._get_or_create_tags(tags, user)
        if work_experiences: self._get_or_create_experiences(work_experiences, user)

        return user

    def _get_or_create_tags(self, tags, user):
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            user.tags.add(tag_obj)

    def _get_or_create_experiences(self, experiences, user):
        auth_user = self.context['request'].user
        for experience in experiences:
            experience_obj, created = WorkExperience.objects.get_or_create(
                user=auth_user,
                **experience,
            )
            user.work_experiences.add(experience_obj)

    def _get_or_create_projects(self, projects, user):
        auth_user = self.context['request'].user
        for project in projects:
            project_obj, created = WorkExperience.objects.get_or_create(
                user=auth_user,
                **project,
            )
            user.projects.add(project_obj)

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs