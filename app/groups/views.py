'''
Views for logical of Groups.
'''

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import Group, User, Post
from .serializers import GroupSerializer
from posts.serializers import PostSerializer

class GroupViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin
):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
         return self.queryset.filter(creator=self.request.user).order_by('-created')
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class AddAdminViewSet(APIView):
    """Allow the authenticated user add to other user for manage group."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response({"detail": "Group not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        if group.admins.filter(id=request.user.pk).exists():
            pk_from_user = request.data['id']

            if User.objects.filter(pk=pk_from_user).exists():
                user = User.objects.get(pk=pk_from_user)

                if group.admins.filter(pk=pk_from_user).exists():
                    return Response({"detail": f"The User with the pk: {pk_from_user} is already admin."})
                
                group.admins.add(user)
                return Response({"detail": f"Now you've added to {user.get_full_name}"}, status=status.HTTP_200_OK)
            
            return Response({"detail": f"User with pk: {pk_from_user} doesn't exists."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "You must be admin in this group for add to new user."})

class GetPostAtGroupViewSet(APIView):
    """Allow the authenticated user get posts at group."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        posts = Post.objects.filter(group=pk)
        serializer = PostSerializer(posts, many=True)

        return Response({'posts': serializer.data})