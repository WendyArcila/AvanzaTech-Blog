from rest_framework import serializers 
from comment.models import BlogComments

class CommentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = BlogComments
        fields = ['id', 'author', 'blog_post', 'comment', 'created_date']
        read_only_fields = ['id', 'author',  'created_date']
        