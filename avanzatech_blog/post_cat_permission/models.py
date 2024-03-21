from django.db import models
from blog_post.models import BlogPost
from category.models import Category
from permission.models import Permission
# Create your models here.

class PostCategoryPermission(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete = models.CASCADE, related_name = 'post_category_permissions')
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete = models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['blog_post', 'category'], name='unique_post_category')
        ]
        
    def __str__(self) -> str:
        return f"{self.category.name} {self.permission.name} {self.blog_post.id}"