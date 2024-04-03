from blog_post.models import BlogPost
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser



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
        #import pdb; pdb.set_trace()
        if isinstance(self.request.user, AnonymousUser):
            queryset = BlogPost.objects.filter(
                post_category_permissions__category__name = "Public",
                post_category_permissions__permission__name__in = permissions,)
        elif self.request.user.is_admin:
            queryset = BlogPost.objects.all()
        else: 
            queryset = BlogPost.objects.filter(
                self.filtered_authenticated(permissions)|
                self.filtered_author( permissions)  |
                self.filtered_team( permissions) 
            )
        return queryset
    
    """ def has_edit_permission(self):
        permissions = "Edit"
        
        if isinstance(self.request.user, AnonymousUser):
            if (BlogPost.objects.filter(
                post_category_permissions__category__name = "Public",
                post_category_permissions__permission__name = "Edit")
                ).exists():
                    return True
            else:
                return False
        elif not self.request.user.is_admin:
            
            if (BlogPost.objects.filter(
                self.filtered_authenticated("Edit")|
                self.filtered_author("Edit") |
                self.filtered_team("Edit")
            )).exists():
                return True
            else:
                print(self.filtered_author( permissions))
                return False
        else:
            return True
"""
    def has_edit_permission(self, instance):
        if isinstance(self.request.user, AnonymousUser):
            permission = instance.post_category_permissions.filter(
            category__name="Public", permission__name="Edit"
            ).first()
            # Verificamos si permission es None, lo que indicaría que no se encontró ninguna coincidencia.
            return permission is not None
        elif self.request.user.is_admin :
            return True
        elif self.request.user.email == instance.author.email:
            permission = instance.post_category_permissions.filter(
            category__name="Author", permission__name="Edit"
            ).first()
            return permission is not None
        elif self.request.user.team == instance.author.team:
            permission = instance.post_category_permissions.filter(
            category__name="Team", permission__name="Edit"
            ).first()
            return permission is not None
        else:
            permission = instance.post_category_permissions.filter(
            category__name="Authenticated", permission__name="Edit"
            ).first()
            return permission is not None