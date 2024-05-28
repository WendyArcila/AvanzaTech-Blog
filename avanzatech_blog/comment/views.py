
from rest_framework import viewsets
from comment.api.serializers import CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from comment.api.filters import CommentsFilter
from blog_post.api.mixin import CustomPermissionMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from comment.api.pagination import CustomPaginationForComments
from rest_framework import status
from comment.models import BlogComments
from django.db.models import Subquery, OuterRef
from django.shortcuts import get_object_or_404


class CommentViewSet(CustomPermissionMixin, viewsets.ModelViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        blog_posts = super().get_queryset(["ReadOnly", "Edit"])
        comments = BlogComments.objects.filter(
            blog_post__in=Subquery(blog_posts.values('id')))
        return comments.order_by('-created_date')

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
    filterset_class = CommentsFilter
    pagination_class = CustomPaginationForComments
