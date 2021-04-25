from django.db import models
from datetime import datetime

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

    @staticmethod
    def save_tasks(tasks, process_id):
        tasks['name'] = tasks['name'][1:]
        for i in range(len(tasks['name'])):
            Task.objects.create(status=tasks['new_status_state'][i], deadline=datetime.strptime(tasks['date'][i], '%Y-%m-%d'), template_id=tasks['task_id'][i],process_id=process_id)
