from django.db import models

class ProcessTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)

class Process(models.Model):
    name = models.CharField(max_length=200)
    template = models.ForeignKey(ProcessTemplate, on_delete=models.PROTECT)

class TaskTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    all_or_any = models.BooleanField()
    choice = models.CharField(max_length=200)

class Task(models.Model):
    output = models.CharField(max_length=200)
    deadline = models.DateTimeField(max_length=200)
    status = models.CharField(max_length=200)
    template = models.ForeignKey(TaskTemplate, on_delete=models.PROTECT)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)

class TaskSequence(models.Model):
    parent = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE, related_name='parent')
    child = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE, related_name='child')
