from django.db import models

from .task_template import TaskTemplate
from .process_template import ProcessTemplate

class TaskSequence(models.Model):
    parent = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE, related_name='parent')
    children = models.ManyToManyField(TaskTemplate)
    process_template = models.ForeignKey(ProcessTemplate, on_delete=models.CASCADE, default=1)
