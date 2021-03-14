from django.db import models

class ProcessTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)

class Process(models.Model):
    name = models.CharField(max_length=200)
    template = models.ForeignKey(ProcessTemplate, on_delete=models.PROTECT)

