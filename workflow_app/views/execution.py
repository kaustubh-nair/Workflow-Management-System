from typing import Counter, Reversible
from django import template
from django.http.response import HttpResponseNotAllowed, HttpResponseRedirect
from django.urls import reverse
from workflow_app.models import role
from workflow_app.models import process_template
from workflow_app.models import actor
from workflow_app.models import task_template
from workflow_app.models.actor import Actor
from workflow_app.models.process_template import ProcessTemplate
from workflow_app.models.task_template import TaskTemplate
from django.shortcuts import render
from datetime import date, datetime, timezone
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from workflow_app.templatetags.extra_tags import *

from ..models import Role
from ..models import Task
from ..models import Process

@login_required
def change_exec_name(request, execution_id):
    current_exec = Process.objects.filter(id=execution_id)
    current_exec.update(name = request.POST['execname'])
    current_exec.get().save()
    return HttpResponseRedirect(reverse('executionindex', args=(execution_id,)))
    
@login_required
def change_deadline(request, execution_id, task_id):
    current_task = Task.objects.filter(id=task_id)
    current_task.update(deadline = request.POST['deadline_change'])
    current_task.get().save()
    return HttpResponseRedirect(reverse('executionindex', args=(execution_id,)))

@login_required
def reset_from(request, execution_id, task_id):
    current_task = Task.objects.filter(id=task_id).get() # For sure a task will be given
    current_task.output = ""
    current_task.deadline = timezone.now()
    current_task.status = "Started"
    actors_list = Actor.objects.filter(task__id = current_task.id)
    for actor in actors_list:
        current_task.actors.remove(actor)
    current_task.save()
    current_task_template = current_task.template
    print(current_task_template)
    # return HttpResponse("LOL")
    next_task_template = current_task_template.children.all()
    try:
        next_task_template = next_task_template.get()
    except TaskTemplate.DoesNotExist:
        next_task_template = None
    while(next_task_template):
        next_task = Task.objects.filter(template = next_task_template, process__id = execution_id ).get()
        next_task.output = ""
        next_task.deadline = timezone.now()
        next_task.status = "Not Started"
        actors_list = Actor.objects.filter(task__id = next_task.id)
        for actor in actors_list:
            next_task.actors.remove(actor)
        next_task.save()
        next_task_template = next_task_template.children.all()
        try:
            next_task_template = next_task_template.get()
        except TaskTemplate.DoesNotExist:
            next_task_template = None
    
    return HttpResponseRedirect(reverse('executionindex',args=(execution_id,)))
        

@login_required
def delete_exec(request, execution_id):
    current_exec = Process.objects.filter(id=execution_id).get()
    current_template = current_exec.template
    list_of_tasks = Task.objects.filter(process = current_exec)
    for task in list_of_tasks:
        task.delete()
    
    current_exec.delete()

    return HttpResponseRedirect(reverse('viewexecs',args=(current_template.id,)))

@login_required
def create_exec(request, template_id):
    workflow_template = ProcessTemplate.objects.filter(id=template_id).get()
    current_user = Actor.objects.filter(name = request.user.username).get()
    workflow = Process(name = "Execution "+ workflow_template.name, template = workflow_template, creator = current_user, dateOfCreation = datetime.now())
    workflow.save()
    first = True
    task_templates = TaskTemplate.objects.filter(process_template = workflow_template)
    for task_template in task_templates:
        if first:
            new_task = Task(template = task_template, process = workflow, deadline = datetime.now(), status = "Started")
            first = False
        else:
            new_task = Task(template = task_template, process = workflow, deadline = datetime.now(), status = "Not Started")

        new_task.save()

    return HttpResponseRedirect(reverse('executionindex', args=(workflow.id,)))

@login_required
def reset_exec(request, execution_id):
    tasks = Task.objects.filter(process__id = execution_id)
    for task in tasks:
        task.output = ""
        if (task.template.is_first_task):
            task.status = "Started"
        else:
            task.status = "Not Started"
        task.deadline = timezone.now()
        actors_list = Actor.objects.filter(task__id = task.id)
        for actor in actors_list:
            task.actors.remove(actor)
        task.save()
    return HttpResponseRedirect(reverse('executionindex', args=(execution_id,)))

@login_required
def index(request, exec_id):
    exec_obj = Process.objects.filter(id = exec_id).get()
    task_list = Task.objects.filter(process_id=exec_id)
    ordered_task_template_list = []
    first_task = TaskTemplate.objects.filter(is_first_task = True, process_template = exec_obj.template)
    try:
        first_task = first_task.get()
    except TaskTemplate.DoesNotExist:
        first_task = None

    ordered_task_template_list.append(first_task)
    # next_task = TaskTemplate.objects.filter(children__contains = [first_task]).get()
    next_task = first_task.children.all()
    try:
        next_task = next_task.get()
    except TaskTemplate.DoesNotExist:
        next_task = None
    # print(next_task)
    while(next_task):
        # print(next_task)
        # next_task = next_task.get()
        ordered_task_template_list.append(next_task)
        next_task = next_task.children.all()
        try:
            next_task = next_task.get()
        except TaskTemplate.DoesNotExist:
            next_task = None
        # next_task = TaskTemplate.objects.filter(children__contains = [next_task]).get()

    
    # print(ordered_task_template_list)

    ordered_task_list = []
    for task_template in ordered_task_template_list:
        ordered_task_list.append( Task.objects.filter(template = task_template, process__id = exec_id ).get())
    
    current_user = Actor.objects.filter(name=request.user.get_username())
    
    message = "Task Template is Broken. Cannot complete currently running task bacause no status_states specified"
    action_list = ""
    started_tasks = Task.objects.filter(status = "Started", process_id = exec_id)
    for task in started_tasks:
        action_list += task.template.status_states

    if (action_list!=""):
        message = ""
    
    user_roles = Role.objects.filter(actor__id=current_user.get().id)

    if (request.method=='POST'):
        # print("LOL")
        d = request.POST["deadline_change"]
        task_id = request.POST["task_id"]
        print(task_id, d)
        task = Task.objects.filter(id = task_id).get()
        task.deadline = d
        task.save()
        # task.update(deadline = d)
        HttpResponseRedirect(reverse('executionindex',args=(exec_id,)))

    template = loader.get_template('view_execution.html')
    collapse_show = "collapse show"
    collapse = "collapse"
    context = {
        'exec_obj': exec_obj,
        'task_list' : ordered_task_list,
        'user_roles' : user_roles,
        # 'total_action_list': total_action_list,
        'message' : message
    }
    return HttpResponse(template.render(context,request))

@login_required
def completeTask(request, exec_id, task_id, action):
    # Getting Current Task and Next Task Objects
    current_process = Process.objects.filter(id=exec_id)
    current_task = Task.objects.filter(id=task_id)
    current_task_template = current_task.get().template
    # current_task_template_actions = current_task_template.status_states
    # print(parse_csv(current_task_template_actions))
    # return HttpResponseRedirect(reverse('executionindex', args=(exec_id,)))
    if(current_task_template.children.filter()):
        next_task_template = current_task_template.children.get()
        next_task = Task.objects.filter(process_id=exec_id, template_id = next_task_template.id)
    else:
        next_task_template = None
        next_task = None
        

    # Add Current Actor the list of actors in current task 
    if(current_task_template.all_or_any == True):
        to_check = Actor.objects.filter(roles__id = current_task_template.role.id)
        if(Counter(to_check)==Counter(Actor.objects.filter(task__id=current_task.get().id))):
            # All Actors done, mark complete
            action_user = Actor.objects.filter(name=request.user.get_username())
            current_task.get().actors.add(action_user.get())
            # current_task.get().save()
            out = current_task.get().output + action_user.get().name + ":" + action + ";"
            # print(out)
            current_task.update(output = out)
            # current_task.get().save()

            current_task.update(status = "Completed")
            current_task.get().save()

            if(next_task):
                next_task.update(status = "Started")
                next_task.get().save()
            
            return HttpResponseRedirect(reverse('executionindex', args=(exec_id,)))
        else:
            action_user = Actor.objects.filter(name=request.user.get_username())
            current_task.get().actors.add(action_user.get())
            # current_task.get().save()
            out = current_task.get().output + action_user.get().name + " : " + action + ","
            # print(out)
            current_task.update(output = out)            
            current_task.get().save()

            if(Counter(to_check)==Counter(Actor.objects.filter(task__id=current_task.get().id))):
                current_task.update(status = "Completed")
                current_task.get().save()

                if(next_task):
                    next_task.update(status = "Started")
                    next_task.get().save()

            return HttpResponseRedirect(reverse('executionindex', args=(exec_id,)))
    else:
        action_user = Actor.objects.filter(name=request.user.get_username())
        current_task.get().actors.add(action_user.get())
        # current_task.get().save()
        out = current_task.get().output + action_user.get().name + ":" + action + ";"
        # print(out)
        current_task.update(output = out)
        # current_task.get().save()

        current_task.update(status = "Completed")
        current_task.get().save()

        if(next_task):
            next_task.update(status = "Started")
            next_task.get().save()
        
        return HttpResponseRedirect(reverse('executionindex', args=(exec_id,)))
