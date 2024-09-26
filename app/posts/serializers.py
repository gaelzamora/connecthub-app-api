# Serializers for posts with API VIEW

from rest_framework import serializers
from core.models import Post

class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts."""

    class Meta:
        model = Post
        fields = ['autor', 'content', 'posted', 'updated', 'likes', 'like_count']
        read_only_fields = ['id', 'autor']
        