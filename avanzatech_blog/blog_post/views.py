from blog_post.api.pagination import CustomPaginationForPost
from post_like.api.pagination import CustomPaginationForPostLikes
from .models import BlogPost
from rest_framework.response import Response
from .api.serializers import BlogPostListCreateSerializer, BlogPostIdSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics, status
from user.permission import AllowPublicEdit
from blog_post.api.mixin import CustomPermissionMixin


class BlogPostListCreate(CustomPermissionMixin, generics.ListCreateAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BlogPostListCreateSerializer

    def get_queryset(self):
        return super().get_queryset(["ReadOnly", "Edit"]).order_by('-created_date')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    pagination_class = CustomPaginationForPost
    
    
class BlogPostRetrieveUpdateDeleteView(
        CustomPermissionMixin,
        generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowPublicEdit]
    serializer_class = BlogPostIdSerializer

    def get_queryset(self):
        return super().get_queryset(["ReadOnly", "Edit"])

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not super().has_edit_permission(instance):
            return Response(
                {"detail": "You do not have permission to edit this post."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        if not super().has_edit_permission(instance):
            return Response(
                {
                "detail": "You do not have permission to delete this post."},
                status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=204)

    def perform_destroy(self, instance):
        instance.delete()
