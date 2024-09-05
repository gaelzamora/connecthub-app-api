"""
Serializers for the user API VIEW.
"""

from django.contrib.auth import (
    get_user_model,
    authenticate
)
from django.utils.translation import gettext as _

from core.models import Tag

from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'first_name', 'last_name', 'tags']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encripted password."""
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    def _get_or_create_tags(self, tags, user):
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            user.tags.add(tag_obj)


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