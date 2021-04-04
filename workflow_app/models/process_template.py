from django.db import models

class ProcessTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    tasks = models.ManyToManyField('TaskTemplate')

