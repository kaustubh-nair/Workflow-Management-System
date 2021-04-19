from workflow_app.models.process_template import ProcessTemplate
from django.db import models
from django.db.models.deletion import PROTECT

from .role import Role

class TaskTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    all_or_any = models.BooleanField(default=False)
    choice = models.CharField(max_length=200, blank=True)
    role = models.ForeignKey(Role, on_delete=PROTECT)
    process_template = models.ForeignKey(ProcessTemplate, on_delete=PROTECT)
    is_first_task = models.BooleanField(default=False)
    children = models.ManyToManyField("TaskTemplate")
    status_states = models.CharField(max_length=10000, default='')

    @staticmethod
    def build_tasks(request):
        tasks = {}
        # Tasks are defined in form numberlabel
        for k,v in request.items():
            if k[0].isdigit():
                task_number = TaskTemplate.get_task_number_from_param(k)
                keyword = [k[1:] if not k[1].isdigit() else k[2:]][0]

                if task_number not in tasks:
                    tasks[task_number] = {}

                if keyword in ['name', 'description', 'all_or_any', 'choice', 'role', 'status_states']:
                    tasks[task_number][keyword] = v[0]
        return tasks

    @staticmethod
    def add_new_task(tasks, request):
        task = {}
        for k,v in request.items():
            if (k.startswith('new_task')):
                keyword = k[9:]
                print(keyword)
                if keyword in ['name', 'description', 'all_or_any', 'choice', 'role', 'status_states']:
                    task[keyword] = v[0]

        index = [max(tasks.keys())+1 if tasks.keys() else 1][0]
        tasks[index] = task
        return tasks

    @staticmethod
    def get_task_number_from_param(param):
        task_number = int([param[0] if not param[1].isdigit() else param[0:2]][0])
        return task_number
