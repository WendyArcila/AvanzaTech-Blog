from django.db import models
from blog_post.models import BlogPost
from category.models import Category
# Create your models here.

class PostCategoryPermission(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.SET(None))
    #permission = 
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['blog_post', 'category'], name='unique_post_category')
        ]