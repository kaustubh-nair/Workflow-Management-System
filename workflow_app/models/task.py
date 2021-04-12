from django.db import models

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
    def build_tasks(request):
        tasks = {}
        # Tasks are defined in form numberlabel
        for k,v in dict(request.GET).items():
            if (k.startswith('task')):
                task_number = int(k[4:6])

                if task_number not in tasks:
                    tasks[task_number] = {}

                keyword = k[6:]
                if keyword == 'name':
                    tasks[task_number]['name'] = v[0]
                elif keyword == 'description':
                    tasks[task_number]['description'] = v[0]
                elif keyword == 'all_or_any':
                    tasks[task_number]['all_or_any'] = v[0]
                elif keyword == 'choice':
                    tasks[task_number]['choice'] = v[0]
                elif keyword == 'role':
                    tasks[task_number]['role'] = v[0]
        return tasks
