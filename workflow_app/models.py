from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=200)

class ProcessTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    tasks = models.ManyToManyField('TaskTemplate')

class Process(models.Model):
    name = models.CharField(max_length=200)
    template = models.ForeignKey(ProcessTemplate, on_delete=models.PROTECT)

class TaskTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    all_or_any = models.BooleanField()
    choice = models.CharField(max_length=200)
    roles = models.ManyToManyField(Role)

class Actor(models.Model):
    name = models.CharField(max_length=200)
    roles = models.ManyToManyField(Role)

class Task(models.Model):
    output = models.CharField(max_length=200)
    deadline = models.DateTimeField(max_length=200)
    status = models.CharField(max_length=200)
    template = models.ForeignKey(TaskTemplate, on_delete=models.PROTECT)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    actors = models.ManyToManyField(Actor)

class TaskSequence(models.Model):
    parent = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE, related_name='parent')
    child = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE, related_name='child')
