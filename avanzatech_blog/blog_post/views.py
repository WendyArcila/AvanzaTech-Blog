
from rest_framework import generics
from .models import BlogPost
from .api.serializers import BlogPostListSerializer, BlogPostCreateSerializer

# Create your views here.


class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BlogPostCreateSerializer
        return BlogPostListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
