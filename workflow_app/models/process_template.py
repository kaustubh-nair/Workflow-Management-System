from workflow_app.models.actor import Actor
from django.db.models.deletion import CASCADE, PROTECT
from workflow_app.models.task_template import TaskTemplate
from workflow_app.models.task_sequence import TaskSequence
from django.db import models


class ProcessTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    firstTask = models.ForeignKey(TaskTemplate, on_delete=CASCADE)
    creator = models.ForeignKey(Actor, on_delete=PROTECT)