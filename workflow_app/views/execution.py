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
def delete_exec(request, execution_id):
    # return HttpResponse("LOL")
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

    # return HttpResponse("NEW PAGE")
    return HttpResponseRedirect(reverse('executionindex', args=(workflow.id,)))

@login_required
def index(request, exec_id):
    exec_obj = Process.objects.filter(id = exec_id).get()
    task_list = Task.objects.filter(process_id=exec_id)
    # total_action_list = []
    # for task in task_list:
    #     task_template = task.template
    #     task_template_actions = task_template.status_states
    #     action_list = parse_csv(task_template_actions)
    #     total_action_list.append(action_list)
    current_user = Actor.objects.filter(name=request.user.get_username())
    
    # print(total_action_list)
    message = "Task Template is Broken. Cannot complete currently running task bacause no status_states specified"
    action_list = ""
    started_tasks = Task.objects.filter(status = "Started", process_id = exec_id)
    for task in started_tasks:
        action_list += task.template.status_states

    # print(action_list)

    if (action_list!=""):
        message = ""
    
    # print(Role.objects.filter(actor__id=current_user.get().id))
    user_roles = Role.objects.filter(actor__id=current_user.get().id)
    # print(user_roles)

    template = loader.get_template('view_execution.html')
    collapse_show = "collapse show"
    collapse = "collapse"
    context = {
        'exec_obj': exec_obj,
        'task_list' : task_list,
        'user_roles' : user_roles,
        # 'total_action_list': total_action_list,
        'message' : message
    }
    # return HttpResponse(output)
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

    next_task_template = current_task_template.children.get()
    next_task = Task.objects.filter(process_id=exec_id, template_id = next_task_template.id)

    # Add Current Actor the list of actors in current task 
    if(current_task_template.all_or_any == True):
        to_check = Actor.objects.filter(roles__id = current_task_template.role.id)
        if(Counter(to_check)==Counter(Actor.objects.filter(task__id=current_task.get().id))):
            # All Actors done, mark complete
            action_user = Actor.objects.filter(name=request.user.get_username())
            current_task.get().actors.add(action_user.get())
            # current_task.get().save()
            out = current_task.get().output + action_user.get().name + ":" + action + ";"
            print(out)
            current_task.update(output = out)
            # current_task.get().save()

            current_task.update(status = "Completed")
            current_task.get().save()

            next_task.update(status = "Started")
            next_task.get().save()
            
            return HttpResponseRedirect(reverse('executionindex', args=(exec_id,)))
        else:
            action_user = Actor.objects.filter(name=request.user.get_username())
            current_task.get().actors.add(action_user.get())
            # current_task.get().save()
            out = current_task.get().output + action_user.get().name + " : " + action + "; <br>"
            print(out)
            current_task.update(output = out)            
            current_task.get().save()

            if(Counter(to_check)==Counter(Actor.objects.filter(task__id=current_task.get().id))):
                current_task.update(status = "Completed")
                current_task.get().save()

                next_task.update(status = "Started")
                next_task.get().save()

            return HttpResponseRedirect(reverse('executionindex', args=(exec_id,)))
    else:
        action_user = Actor.objects.filter(name=request.user.get_username())
        current_task.get().actors.add(action_user.get())
        # current_task.get().save()
        out = current_task.get().output + action_user.get().name + ":" + action + ";"
        print(out)
        current_task.update(output = out)
        # current_task.get().save()

        current_task.update(status = "Completed")
        current_task.get().save()

        next_task.update(status = "Started")
        next_task.get().save()
        
        return HttpResponseRedirect(reverse('executionindex', args=(exec_id,)))
