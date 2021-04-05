from django.db import models


class ProcessTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    first_task = models.ForeignKey('Task', on_delete=models.PROTECT, default=1)

