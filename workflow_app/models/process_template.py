from workflow_app.models.actor import Actor
from django.db.models.deletion import CASCADE, PROTECT
from django.db import models


class ProcessTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    creator = models.ForeignKey(Actor, on_delete=PROTECT)
    dateOfCreation = models.DateField(max_length=200)
