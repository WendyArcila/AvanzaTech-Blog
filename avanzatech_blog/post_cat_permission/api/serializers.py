from post_cat_permission.models import PostCategoryPermission
from rest_framework import serializers 
from permission.models import Permission
from category.models import Category

class CategoryPostPermissionSerializer(serializers.ModelSerializer):
    permission = serializers.PrimaryKeyRelatedField(queryset = Permission.objects.all() )
    category = serializers.PrimaryKeyRelatedField(queryset = Category.objects.all() )
    class Meta:
        model = PostCategoryPermission
        fields = ['permission',  'category']
    
""" def to_representation(self, instance):
        return{
            'permission' :instance.permission.name,
            'category': instance.category.name            
        } """
