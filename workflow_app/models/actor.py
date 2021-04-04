from django.db import models

from .role import Role

class Actor(models.Model):
    name = models.CharField(max_length=200)
    roles = models.ManyToManyField(Role)

