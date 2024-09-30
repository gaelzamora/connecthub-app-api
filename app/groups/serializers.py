
from rest_framework import serializers
from django.utils.translation import gettext as _

from accounts.serializers import UserSerializer, TagSerializer

from core.models import Group

class GroupSerializer(serializers.ModelSerializer):
    """Serializer for groups."""

    admins = UserSerializer(many=True, required=False)
    users = UserSerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Group
        fields = ['id', 'name', 'creator', 'admins', 'users', 'tags']
        read_only_fields = ['id', 'creator']

    def create(self, validated_data):
        group = Group.objects.create(**validated_data)
        print(validated_data)
        group.admins.add(validated_data['creator'])

        return group