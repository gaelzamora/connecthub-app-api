# Serializers for posts with API VIEW

from rest_framework import serializers
from django.utils.translation import gettext as _

from core.models import Hashtag, Post

class HashTagSerializer(serializers.ModelSerializer):
    """Serializer for hashtags."""

    class Meta:
        model = Hashtag 
        fields = ['id', 'name']
        read_only_fields = ['id']

class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts."""
    hashtags = HashTagSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'group', 'author', 'content', 'posted', 'updated', 'likes', 'like_count', 'hashtags']
        read_only_fields = ['id', 'author']

    def create(self, validated_data):
        """Create and return post with all hashtags created."""
        hashtags = validated_data.pop('hashtags', [])
        post = Post.objects.create(**validated_data)
        self._get_or_create_hashtags(hashtags, post)

        return post
    
    def _get_or_create_hashtags(self, hashtags_data, post):
        """Helper method to create or get technologies and assign them to the project."""
        for hashtag in hashtags_data:
            name = hashtag.get('name')
            obj, created = Hashtag.objects.get_or_create(
                name=name,
                user=post.author
            )
            post.hashtags.add(obj)
