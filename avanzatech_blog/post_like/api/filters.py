import django_filters
from post_like.models import PostLike

class PostLikeFilter(django_filters.FilterSet):
    class Meta:
        model = PostLike
        fields = ['blog_post', 'author']