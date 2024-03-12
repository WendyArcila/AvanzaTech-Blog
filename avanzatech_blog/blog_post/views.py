
from rest_framework import generics
from .models import BlogPost
from rest_framework.response import Response
from .api.serializers import BlogPostCreateSerializer, BlogPostIdSerializer

# Create your views here.

class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostCreateSerializer
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        


class BlogPostRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostIdSerializer
    
    def get_serializer_class(self):
            if self.request.method in ['PUT', 'PATCH']:
                return BlogPostIdSerializer
            return super().get_serializer_class()

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)

    def perform_destroy(self, instance):
        instance.delete()
