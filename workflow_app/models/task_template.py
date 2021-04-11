from django.db import models
from django.db.models.deletion import PROTECT

from .role import Role
from .process_template import ProcessTemplate
from .task_template import TaskTemplate

class TaskTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    all_or_any = models.BooleanField()
    choice = models.CharField(max_length=200)
    role = models.ForeignKey(Role, on_delete=PROTECT)
    process_template = models.ForeignKey(ProcessTemplate, on_delete=models.CASCADE)
    is_first_task = models.BooleanField(default=False)
    children = models.ManyToManyField(TaskTemplate)
