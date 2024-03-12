from rest_framework import serializers 
from blog_post.models import BlogPost
from post_cat_permission.models import PostCategoryPermission
from permission.models import Permission
from category.models import Category
from user.api.serializers import UserSerializer
from post_cat_permission.api.serializers import CategoryPostPermissionSerializer
from rest_framework.exceptions import ValidationError

''' Se recibe un diccionario de permissions en orden de las categorías
en las que se van a crear las instancias de cat_post_permi, se guarda el autor
como quien está autenticado y además se guarda en excerpt los 200 primeros caracteres del post 
'''
    
class BlogPostCreateSerializer(serializers.ModelSerializer):
    
    post_category_permission = CategoryPostPermissionSerializer(many=True, source ='post_category_permissions')
    class Meta:
        model = BlogPost
        fields = ['author', 'title', 'content', 'excerpt','post_category_permission' ]
        read_only_fields = ['author', 'excerpt']

    


    def create(self, validated_data):
        
        def validate(self, data):
            if 'post_category_permission' not in data or not data['post_category_permission']:
                raise ValidationError("Permission are necessary to create a post.")
            return data
        
        permissions_data = validated_data.pop('post_category_permissions')
        blog_post = BlogPost.objects.create(**validated_data)
        excerpt = blog_post.content[:200]
        blog_post.excerpt = excerpt
        blog_post.save()
        
        print("esta es la categoría mirar acáaaaaaaa: ", permissions_data)
        
        # Crear automáticamente 4 instancias de Category_Post_Permission
        for permission_data in permissions_data:
            category_id = permission_data.get('category').id
            category = Category.objects.get(pk=category_id)
            permission_id = permission_data.get('permission').id
            permission = Permission.objects.get(pk=permission_id)
            # Ahora asignamos correctamente 'blog_post' a cada PostCategoryPermission
            PostCategoryPermission.objects.create(blog_post=blog_post, category=category, permission=permission)

        
        return blog_post

    
class BlogPostIdSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post_category_permissions = serializers.SerializerMethodField()   
    
    class Meta: 
        model = BlogPost
        fields = ['id', 'author', 'title', 'content', 'excerpt','post_category_permissions' ]
        read_only_fields = ['author', 'excerpt']

    def update(self, instance, validated_data):
        # Actualizar el título y el contenido del BlogPost
        current_title = instance.title
        current_content = instance.content
        
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        excerpt = instance.content[:200]
        instance.excerpt = excerpt
        instance.save()
        
        title_changed = current_title != instance.title
        content_changed = current_content != instance.content

       # if title_changed or content_changed:
            
        # Actualizar las categorías asociadas, si se proporcionan
        post_category_permissions_data = validated_data.get('post_category_permissions', [])
        if post_category_permissions_data:
            instance.post_category_permissions.set([PostCategoryPermission.objects.get(pk=id) for id in post_category_permissions_data])

        return instance
    
    def get_post_category_permissions(self, obj):
        # Obtiene todos los permisos asociados a obj (un BlogPost)
        # a través de las instancias de PostCategoryPermission.
        permissions = obj.post_category_permissions.select_related('permission').all()
        
        # Devuelve una lista de objetos serializados por CategoryPostPermissionListSerializer
        return CategoryPostPermissionSerializer(permissions, many=True).data
    