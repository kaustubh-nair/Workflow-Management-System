from workflow_app.models.actor import Actor
from django.db import models
from django.db.models.deletion import PROTECT

from .process_template import ProcessTemplate

class Process(models.Model):
    name = models.CharField(max_length=200)
    template = models.ForeignKey(ProcessTemplate, on_delete=models.PROTECT)
    creator = models.ForeignKey(Actor, on_delete=PROTECT)

