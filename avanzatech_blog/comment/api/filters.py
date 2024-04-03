import django_filters
from comment.models import BlogComments

class CommentsFilter(django_filters.FilterSet):
    class Meta:
        model = BlogComments
        fields = ['blog_post', 'author']