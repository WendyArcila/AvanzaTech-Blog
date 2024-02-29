from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Category (models.Model):
    name = models.CharField(_('Name'),max_length = 150)
    description = models.CharField(_('Description'),max_length = 255)
    
    
def __str__(self):
    return self.name