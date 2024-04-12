from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Team (models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(_('Description'))


def __str__(self):
    return f"{self.name}"
