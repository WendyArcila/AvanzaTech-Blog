from rest_framework import serializers
from post_like.models import PostLike


class PostLikeSerializer(serializers.ModelSerializer):
    
    author_name = serializers.CharField(source='author.nick_name', read_only=True)
    
    class Meta:
        model = PostLike
        fields = ['id', 'blog_post', 'author', 'author_name']
        read_only_fields = ['author', 'id', 'author_name']

    def validate(self, data):
        author = self.context['request'].user

        if PostLike.objects.filter(
                blog_post=data['blog_post'],
                author=author).exists():
            raise serializers.ValidationError(
                "This post already has your like.")
        return data
