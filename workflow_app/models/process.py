from workflow_app.models.actor import Actor
from datetime import datetime
from django.db import models
from django.db.models.deletion import PROTECT

from .process_template import ProcessTemplate

class Process(models.Model):
    name = models.CharField(max_length=200)
    template = models.ForeignKey(ProcessTemplate, on_delete=models.PROTECT)
    creator = models.ForeignKey(Actor, on_delete=PROTECT)
    dateOfCreation = models.DateField(max_length=200)

    @staticmethod
    def save_process(req):
        process = Process.objects.create(name=req['name'][0], template=ProcessTemplate.objects.get(id=int(req['process_template_id'][0])), dateOfCreation=datetime.now(), creator_id=1)
        return process.id

