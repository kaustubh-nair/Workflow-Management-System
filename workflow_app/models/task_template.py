from django.db import models

from .role import Role
from .process_template import ProcessTemplate

class TaskTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    all_or_any = models.BooleanField()
    choice = models.CharField(max_length=200)
    roles = models.ManyToManyField(Role)
    process_template = models.ForeignKey(ProcessTemplate, on_delete=models.CASCADE)
    is_first_task = models.BooleanField(default=False)
    children = models.ManyToManyField("TaskTemplate")
