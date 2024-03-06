from rest_framework import serializers 
from blog_post.models import BlogPost
from post_cat_permission.api.serializers import CategoryPostPermissionListSerializer, CategoryPostPermissionCreateSerializer
from post_cat_permission.models import PostCategoryPermission
from permission.models import Permission
from category.models import Category


''' Se recibe un diccionario de permissions en orden de las categorías
en las que se van a crear las instancias de cat_post_permi, se guarda el autor
como quien está autenticado y además se guarda en excerpt los 200 primeros caracteres del post 
'''
class BlogPostListSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()    
    
    class Meta:
        model = BlogPost
        fields = ['author', 'title', 'content', 'excerpt','permissions' ]
        
    
    def get_permissions(self, obj):
        # Obtiene todos los permisos asociados a obj (un BlogPost)
        # a través de las instancias de PostCategoryPermission.
        permissions = obj.post_category_permissions.select_related('permission').all()
        # Devuelve una lista de objetos serializados por CategoryPostPermissionListSerializer
        return CategoryPostPermissionListSerializer(permissions, many=True).data
    
    
class BlogPostCreateSerializer(serializers.ModelSerializer):

    permissions= CategoryPostPermissionCreateSerializer(many=True)
    class Meta:
        model = BlogPost
        fields = ['author', 'title', 'content', 'excerpt','permissions' ]
        read_only_fields = ['author', 'excerpt']


    def create(self, validated_data):
        permissions_data = validated_data.pop('permissions')
        #author=self.context['request'].user, 
        blog_post = BlogPost.objects.create(**validated_data)
        excerpt = blog_post.content[:200]
        blog_post.excerpt = excerpt
        blog_post.save()
        
        # Crear automáticamente 4 instancias de Category_Post_Permission
        for permission_data in permissions_data:
            category_id = permission_data.get('category').id
            category = Category.objects.get(pk=category_id)
            permission_id = permission_data.get('permission').id
            permission = Permission.objects.get(pk=permission_id)
            # Ahora asignamos correctamente 'blog_post' a cada PostCategoryPermission
            PostCategoryPermission.objects.create(blog_post=blog_post, category=category, permission=permission)
 
        
        return blog_post