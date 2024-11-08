"""
Database models
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone

def user_image_file_path(instance, filename):
    """Generate file path for new user image."""
    ext = os.path.split(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'user', filename)

def post_image_file_path(intance, filename):
    """Generate file path for new port image."""
    ext = os.path.split(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'post', filename)

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError('User must have an email Address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    tags = models.ManyToManyField('Tag', related_name='core_user')
    image = models.ImageField(null=True, upload_to=user_image_file_path)
    work_experiences = models.ManyToManyField('WorkExperience', related_name='core_experience')
    projects = models.ManyToManyField('Project', related_name='core_project')
    follows = models.ManyToManyField('self', symmetrical=False , related_name='followers', blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
    
    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email

class Tag(models.Model):
    """Tag for filtering users."""
    name = models.CharField(max_length=255)

    def get_name(self):
        return self.name
    
class WorkExperience(models.Model):
    """Work experience for each user."""
    business = models.CharField(max_length=255)
    year = models.IntegerField(null=True)
    time = models.CharField(max_length=255)
    current_job = models.BooleanField(default=False)
    position = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class Project(models.Model):
    """Projects for each user."""
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    technologies = models.ManyToManyField('Technologie', related_name='technologies')
    year = models.IntegerField(null=True)

class Technologie(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='user_technologie'
    )

    def __str__(self):
        return self.names
    
# Models for posts

class Group(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_group'
    )
    admins = models.ManyToManyField('User', related_name='admin_groups')
    users = models.ManyToManyField('User', related_name='member_groups')
    tags = models.ManyToManyField('Tag', related_name='tag_groups')
    created = models.DateTimeField(auto_now_add=True, null=True)

    def get_name(self):
        return self.name

class Post(models.Model):
    content = models.TextField(max_length=255)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_post'
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        related_name='posts',
        null=True
    )
    posted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    hashtags = models.ManyToManyField('HashTag', related_name='posts')
    image = models.ImageField(null=True, upload_to=post_image_file_path)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='posts',
        blank=True
    )   

    def get_content(self):
        return f'User {self.autor.get_full_name()} - [{self.content}]'
    
class Hashtag(models.Model):
    name = models.CharField(max_length=50, default='fyp')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_hashtag'
    )

    def get_name_message(self):
        return f'You have created a new hashtag {self.name}'