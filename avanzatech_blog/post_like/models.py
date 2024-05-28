from django.db import models
from blog_post.models import BlogPost
from user.models import CustomUser
from django.utils.translation import gettext_lazy as _


class PostLike (models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='post_like')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'blog_post',
                    'author'],
                name='unique_like')]
