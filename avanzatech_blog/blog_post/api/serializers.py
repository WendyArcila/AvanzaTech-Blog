from rest_framework import serializers
from blog_post.models import BlogPost
from comment.api.serializers import CommentSerializer
from post_cat_permission.models import PostCategoryPermission
from permission.models import Permission
from category.models import Category
from post_like.api.serializers import PostLikeSerializer
from user.api.serializers import UserSerializer
from post_cat_permission.api.serializers import CategoryPostPermissionSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import AnonymousUser


class BlogPostListCreateSerializer(serializers.ModelSerializer):

    post_category_permission = CategoryPostPermissionSerializer(
        many=True, source='post_category_permissions')

    author_name = serializers.CharField(source='author.nick_name', read_only=True)
    author_team = serializers.CharField(source='author.team.name', read_only=True)
    likes = PostLikeSerializer(source='post_like', many=True, read_only=True)
    comments = PostLikeSerializer(source='post_comment', many=True, read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id',
            'author',
            'author_name',
            'author_team',
            'likes',
            'comments',
            'title',
            'content',
            'excerpt',
            'created_date',
            'post_category_permission']
        read_only_fields = ['author', 'excerpt', 'id', 'created_date', 'author_name', 'author_team', 'likes', 'comments' ]

    def to_representation(self, instance):
        
        representation= super().to_representation(instance)
        #import pdb; pdb.set_trace()
        if self.context.get('request').user.is_authenticated: 
            
            request = self.context.get('request').user.id
            
            flag = False
            like=instance.post_like.filter(author_id=request)
            if like:
                flag = True
                
            representation['flag'] = flag
    
        return representation
    

    def validate(self, data):
        if 'post_category_permissions' not in data or not data['post_category_permissions']:
            raise ValidationError("Permission are necessary to create a post.")

        if len(data['post_category_permissions']) != 4:
            raise ValidationError("The post needs exactly four permissions.")

        category_ids = [permission_data.get(
            'category').id for permission_data in data['post_category_permissions']]

        if len(category_ids) != len(set(category_ids)):
            raise ValidationError("The category needs to be unique.")

        if not all(1 <= category_id <= 4 for category_id in category_ids):
            raise ValidationError("The category ID must be between 1 and 4.")

        return data

    def create(self, validated_data):

        permissions_data = validated_data.pop('post_category_permissions')
        blog_post = BlogPost.objects.create(**validated_data)

        for permission_data in permissions_data:
            category_id = permission_data.get('category').id
            category = Category.objects.get(pk=category_id)
            permission_id = permission_data.get('permission').id
            permission = Permission.objects.get(pk=permission_id)

            PostCategoryPermission.objects.create(
                blog_post=blog_post, category=category, permission=permission)

        return blog_post


class BlogPostIdSerializer(serializers.ModelSerializer):
    post_category_permission = CategoryPostPermissionSerializer(
        many=True, source='post_category_permissions')
    author = UserSerializer(read_only=True)

    author_name = serializers.CharField(source='author.nick_name', read_only=True)
    author_team = serializers.CharField(source='author.team.name', read_only=True)
    likes = PostLikeSerializer(source='post_like', many=True, read_only=True)
    comments = CommentSerializer(source='post_comment', many=True, read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id',
            'author',
            'author_name',
            'author_team',
            'likes',
            'comments',
            'created_date',
            'title',
            'content',
            'post_category_permission']
        read_only_fields = ['id', 'created_date', 'author', 'author_name', 'author_team', 'likes', 'comments' ]

    def validate(self, data):
        if 'post_category_permissions' not in data or not data['post_category_permissions']:
            raise ValidationError("Permission are necessary to create a post.")

        if len(data['post_category_permissions']) != 4:
            raise ValidationError("The post needs exactly four permissions.")

        category_ids = [permission_data.get(
            'category').id for permission_data in data['post_category_permissions']]
        expected_order = list(range(1, 5))

        # if category_ids != expected_order:
        #     raise ValidationError(
        #         "The category IDs must be in order from 1 to 4.")

        if len(category_ids) != len(set(category_ids)):
            raise ValidationError("The category needs to be unique.")
        # if not all(1 <= category_id <= 4 for category_id in category_ids):
        #     raise ValidationError("The category ID must be between 1 and 4.")

        return data

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()

        post_category_permissions_data = validated_data.get(
            'post_category_permissions', [])
        for permission_data in post_category_permissions_data:
            permission_id = permission_data.get('permission').id
            permission = Permission.objects.get(pk=permission_id)
            category_id = permission_data.get('category').id
            category = Category.objects.get(pk=category_id)

            post_category_permission = instance.post_category_permissions.get(
                category=category)
            post_category_permission.permission = permission
            post_category_permission.save()
        return instance
