"""
Database models
"""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


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
    work_experiences = models.ManyToManyField('WorkExperience', related_name='core_experience')
    projects = models.ManyToManyField('Project', related_name='core_project')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.first_name + self.last_name
    
    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email

class Tag(models.Model):
    """Tag for filtering users."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_tags'
    )
    
class WorkExperience(models.Model):
    """Work experience for each user."""
    business = models.CharField(max_length=255)
    year = models.IntegerField(null=True)
    time = models.CharField(max_length=255)
    current_job = models.BooleanField(default=False)
    position = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_experience'
    )

class Project(models.Model):
    """Projects for each user."""
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    technologies = models.ManyToManyField('Technologie', related_name='project_technologie', blank=True)
    year = models.IntegerField(null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_project'
    )

class Technologie(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
