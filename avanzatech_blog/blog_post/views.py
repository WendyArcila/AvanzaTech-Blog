from .models import BlogPost
from rest_framework.response import Response
from .api.serializers import BlogPostListCreateSerializer, BlogPostIdSerializer
from django.db.models import Q, QuerySet
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics, status
from user.permission import AllowPublicEdit
from blog_post.api.mixin import CustomPermissionMixin


def filtered_authenticated(self, permission):
        return Q(
            post_category_permissions__category__name = "Authenticated",
            post_category_permissions__permission__name__in = permission,
            ) & ~Q(author__email = self.request.user.email
            ) & ~Q(author__team = self.request.user.team
            )

def filtered_author(self, permission):
        return Q(
            author__email = self.request.user.email,
            post_category_permissions__category__name = "Author",
            post_category_permissions__permission__name__in = permission,
        )
        
def filtered_team(self, permission):
        return Q(
            author__team = self.request.user.team,
            post_category_permissions__category__name = "Team",
            post_category_permissions__permission__name__in = permission,
        ) & ~Q(
            author__email = self.request.user.email
        )


class BlogPostListCreate(CustomPermissionMixin, generics.ListCreateAPIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BlogPostListCreateSerializer
    
    def get_queryset(self):
        return super().get_queryset(["ReadOnly","Edit"])
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    


class BlogPostRetrieveUpdateView(CustomPermissionMixin, generics.RetrieveUpdateAPIView):
    permission_classes = [AllowPublicEdit]
    serializer_class = BlogPostIdSerializer
    
    def get_queryset(self):
        return super().get_queryset(["ReadOnly","Edit"])
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(super().has_edit_permission())
        if not (super().has_edit_permission()):
            return Response({"detail": "You do not have permission to edit this post."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if isinstance(self.request.user, AnonymousUser):
            if not (BlogPost.objects.filter(
                post_category_permissions__category__name = "Public",
                post_category_permissions__permission__name__in = "Edit",)
            ).exists():
                
                return Response({"detail": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)

        elif not self.request.user.is_admin:
            if(BlogPost.objects.filter(
                Q(filtered_authenticated(self, "Edit")) |
                Q(filtered_author(self, "Edit"))  |
                Q(filtered_team(self, "Edit"))
            )).exists():
                
                return Response({"detail": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        
        
        self.perform_destroy(instance)
        return Response(status=204)

    def perform_destroy(self, instance):
        instance.delete()
        
    
        
