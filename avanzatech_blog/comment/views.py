
from rest_framework import viewsets
from comment.api.serializers import CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from comment.api.filters import CommentsFilter
from blog_post.api.mixin import CustomPermissionMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from comment.api.pagination import CustomPaginationForComments
from rest_framework import  status


class CommentViewSet(CustomPermissionMixin, viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        blog_posts = super().get_queryset(["ReadOnly","Edit"])
        blog_post_ids = blog_posts.values_list('id')
        # Filtra los objetos 'PostLike' donde 'blog_post_id' esté en la lista de IDs obtenidos.
        return CommentSerializer.Meta.model.objects.filter(blog_post__in=blog_post_ids)
    
    def create (self, request):
        post_id = request.data.get('blog_post')
        
        if not self.get_queryset().filter(blog_post=post_id).exists():
            return Response({"detail": "The post is not available to be comment."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method 'PUT' not allowed."}, status=405)
    
    def partial_update(self, request, *args, **kwargs):
        return Response({"detail": "Method 'PATCH' not allowed."}, status=405)
    
    
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentsFilter
    pagination_class = CustomPaginationForComments