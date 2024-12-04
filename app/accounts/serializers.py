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
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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

    def create(self, validated_data):
        project = validated_data.pop('project')

        new_technologie, created = Technologie.objects.get_or_create(**validated_data)

        project.technologies.add(new_technologie)

        return new_technologie

class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for projects"""
    technologies = TechnologieSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'year', 'technologies']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create and return a project."""
        technologies = validated_data.pop('technologies', [])
        project = Project.objects.create(**validated_data)
        self._get_or_create_technologies(technologies, project)
        
        return project
    
    def update(self, instance, validated_data):
        """Update a project return an instance."""
        technologies = validated_data.pop('technologies', None)
        if technologies is not None:
            instance.technologies.clear()
            self._get_or_create_technologies(technologies, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

    def _get_or_create_technologies(self, technologies_data, project):
        """Helper method to create or get technologies and assign them to the project."""
        for technologie_data in technologies_data:
            technologie_obj, created = Technologie.objects.get_or_create(
                name=technologie_data['name'],
                user=project.user  # Relacionar con el usuario del proyecto
            )
            project.technologies.add(technologie_obj)

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""
    tags = TagSerializer(many=True, source='user_tags', required=False)
    work_experiences = WorkExperienceSerializer(many=True, source='user_experience', required=False)
    projects = ProjectSerializer(many=True, source='user_project', required=False)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'first_name', 'last_name', 'tags', 'work_experiences', 'projects', 'follows']
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
        projects = validated_data.pop('user_projects', None)
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        if tags: self._get_or_create_tags(tags, user)
        if work_experiences: self._get_or_create_experiences(work_experiences, user)
        if projects: self._get_or_create_projects(projects, user)

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

    def get_followers_count(self, obj):
        return obj.followers.count()
    
class UserImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to User"""

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['image']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['first_name'] = user.first_name 
        token['is_staff'] = user.is_staff
        token['projects'] = [project.id for project in user.projects.all()]
        token['tags'] = [tag.id for tag in user.tags.all()]
        token['follows'] = [follow.id for follow in user.follows.all()]
        token['work_experiences'] = [work_experience.id for work_experience in user.work_experiences.all()]
        token['image'] = str(user.image)

        return token
