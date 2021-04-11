from workflow_app.models import role
from workflow_app.models.actor import Actor
from workflow_app.models.process_template import ProcessTemplate
from workflow_app.models.task_template import TaskTemplate
from django.shortcuts import render
from datetime import datetime, timezone
from django.http import HttpResponse
from django.template import loader

from ..models import Role
from ..models import Task
from ..models import Process


def init():
    role1 = Role(name = "Role 1")
    role2 = Role(name = "Role 2")
    actor1 = Actor(name = "Actor 1", roles=[role1])
    actor2 = Actor(name = "Actor 2", roles=[role1, role2])
    actor3 = Actor(name = "Actor 3", roles=[role2])
    pt1 = ProcessTemplate(name = "Process Template 1", descrioption = "Description of Process Template 1")
    pt2 = ProcessTemplate(name = "Process Template 2", descrioption = "Description of Process Template 2")
    tt1 = TaskTemplate(name = "Task Template 1", description = "Description of Task Template 1", all_or_any = False, choice = "Choice 1", role)

def index(request, task_id):
    # procstemp = ProcessTemplate()
    # procstemp.save()
    # procs = Process() 
    # procs.template = procstemp
    # procs.save()
    # tt = TaskTemplate()
    # tt.all_or_any = False
    # tt.save()
    # t1 = Task()
    # t1.deadline = datetime.now()
    # t1.template = tt
    # t1.process = procs 
    # t1.save()
    latest_task_list = Task.objects.all()
    # output = ', '.join([str(q.deadline) for q in latest_task_list])
    # return HttpResponse("This is supposed to be Task ID: %s" % task_id)
    template = loader.get_template('workflow_app/index.html')
    context = {
        'latest_task_list' : latest_task_list,
    }
    # return HttpResponse(output)
    return HttpResponse(template.render(context,request))


