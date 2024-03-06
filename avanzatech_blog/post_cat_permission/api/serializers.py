from post_cat_permission.models import PostCategoryPermission
from rest_framework import serializers 
from permission.models import Permission
from blog_post.models import BlogPost
from category.models import Category

class CategoryPostPermissionListSerializer(serializers.ModelSerializer):
    permission = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all())
    blog_post = serializers.PrimaryKeyRelatedField(queryset=BlogPost.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = PostCategoryPermission
        fields = ['permission', 'blog_post', 'category']
        
        
class CategoryPostPermissionCreateSerializer(serializers.ModelSerializer):
    permission = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = PostCategoryPermission
        fields = ['permission', 'category']
        
        
