from django.db import models

from .role import Role

class TaskTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    all_or_any = models.BooleanField()
    choice = models.CharField(max_length=200)
    roles = models.ManyToManyField(Role)

