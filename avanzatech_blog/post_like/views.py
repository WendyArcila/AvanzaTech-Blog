
from rest_framework import viewsets
from post_like.api.serializers import PostLikeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from post_like.api.filters import PostLikeFilter
from blog_post.api.mixin import CustomPermissionMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from post_like.api.pagination import CustomPaginationForPostLikes
from post_like.models import PostLike
from rest_framework import status
from django.db.models import Subquery
from django.shortcuts import get_object_or_404


class PostLikeViewSet(CustomPermissionMixin, viewsets.ModelViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostLikeSerializer

    def get_queryset(self):
        blog_posts = super().get_queryset(["ReadOnly", "Edit"])
        likes = PostLike.objects.filter(
            blog_post__in=Subquery(blog_posts.values('id')))
        return likes.order_by('id')

    def create(self, request):
        post_id = request.data.get('blog_post')
        blog_posts = CustomPermissionMixin.get_queryset(
            self, ['ReadOnly', 'Edit'])
        get_object_or_404(blog_posts, pk=post_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method 'PUT' not allowed."}, status=405)

    def partial_update(self, request, *args, **kwargs):
        return Response({"detail": "Method 'PATCH' not allowed."}, status=405)

    def retrieve(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method 'RETRIEVE' not allowed."}, status=405)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # import pdb; pdb.set_trace()

        if request.user != instance.author:
            return Response({"message": "Only author can delete this object"},
                            status=status.HTTP_401_UNAUTHORIZED)

        super().destroy(request, *args, **kwargs)
        return Response({"message": "Object successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)

    filter_backends = [DjangoFilterBackend]
    filterset_class = PostLikeFilter
    pagination_class = CustomPaginationForPostLikes
