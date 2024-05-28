from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import CustomUser
from blog_post.models import BlogPost
from django.utils import timezone


class BlogComments(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='post_comment')
    comment = models.CharField(_('comment text'), max_length=255)
    created_date = models.DateTimeField(default=timezone.now)



