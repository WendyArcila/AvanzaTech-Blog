from blog_post.models import BlogPost
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from rest_framework.response import Response
from rest_framework import  status


class CustomPermissionMixin():
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
        
    def get_queryset(self, permissions): 
        if isinstance(self.request.user, AnonymousUser):
            queryset = BlogPost.objects.filter(
                post_category_permissions__category__name = "Public",
                post_category_permissions__permission__name__in = permissions,)
        elif self.request.user.is_admin:
            queryset = BlogPost.objects.all()
        else: 
            queryset = BlogPost.objects.filter(
                Q(self.filtered_authenticated(permissions)) |
                Q(self.filtered_author( permissions))  |
                Q(self.filtered_team( permissions))
            )
        return queryset
    
    def has_edit_permission(self):
        """
        Verifica si el usuario tiene permiso para editar el post específico.
        """
        permissions = ['Edit']
        
        if isinstance(self.request.user, AnonymousUser):
            if (BlogPost.objects.filter(
                post_category_permissions__category__name = "Public",
                post_category_permissions__permission__name__in = "Edit",)
            ).exists():
                return True
        elif not self.request.user.is_admin:
            print(BlogPost.objects.filter(
                Q(self.filtered_authenticated(permissions)) |
                Q(self.filtered_author(permissions))  |
                Q(self.filtered_team(permissions))
            ))
            if(BlogPost.objects.filter(
                Q(self.filtered_authenticated(permissions)) |
                Q(self.filtered_author(permissions))  |
                Q(self.filtered_team(permissions))
            )).exists():
                return True
        else:
            return False
