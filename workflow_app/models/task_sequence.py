from django.db import models

from .task_template import TaskTemplate

class TaskSequence(models.Model):
    parent = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE, related_name='parent')
    child = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE, related_name='child')
