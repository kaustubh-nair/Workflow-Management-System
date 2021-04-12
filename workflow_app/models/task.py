from django.db import models

from .task_template import TaskTemplate
from .process import Process
from .actor import Actor

class Task(models.Model):
    output = models.CharField(max_length=200)
    deadline = models.DateTimeField(max_length=200)
    status = models.CharField(max_length=200)
    template = models.ForeignKey(TaskTemplate, on_delete=models.PROTECT)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    actors = models.ManyToManyField(Actor)
