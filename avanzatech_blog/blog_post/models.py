from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone  
from user.models import CustomUser
from permission.models import Permission 

# Create your models here.
class BlogPost(models.Model):
    author = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    title = models.CharField(_('post title'),max_length = 100)
    content = models.TextField(_('post content'))
    excerpt = models.CharField(max_length = 200)
    created_date = models.DateTimeField(default = timezone.now) 
    updated_date = models.DateTimeField(default = timezone.now)
    
def __str__(self):
    return self.content 
