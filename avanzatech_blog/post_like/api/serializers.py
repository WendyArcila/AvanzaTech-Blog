from rest_framework import serializers 
from blog_post.models import BlogPost
from post_like.models import PostLike


class PostLikeListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['id','blog_post', 'author']
        read_only_fields = ['author', 'id']
        
    