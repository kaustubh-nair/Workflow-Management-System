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


def init():
    role1 = Role(name = "Role 1")
    role1.save()
    role2 = Role(name = "Role 2")
    role2.save()
    
    actor1 = Actor(name = "Actor 1")
    actor1.save()
    actor1.roles.add(role1)
    actor1.save()
    actor2 = Actor(name = "Actor 2")
    actor2.save()
    actor2.roles.add(role1)
    actor2.roles.add(role2)
    actor2.save()
    actor3 = Actor(name = "Actor 3")
    actor3.save()
    actor3.roles.add(role2)
    actor3.save()
    
    pt1 = ProcessTemplate(name = "Process Template 1", description = "Description of Process Template 1", creator = actor1, dateOfCreation = datetime.now())
    pt1.save()
    pt2 = ProcessTemplate(name = "Process Template 2", description = "Description of Process Template 2", creator = actor1, dateOfCreation = datetime.now())
    pt2.save()

    tt11 = TaskTemplate(name = "Task Template 11", description = "Description of Task Template 11", all_or_any = False, choice = "Choice 11", role=role1, process_template = pt1, is_first_task = True)
    tt11.save()
    tt12 = TaskTemplate(name = "Task Template 12", description = "Description of Task Template 12", all_or_any = True, choice = "Choice 12", role=role2, process_template = pt1, is_first_task = False)
    tt12.save()
    tt11.children.add(tt12)
    tt11.save()
    tt13 = TaskTemplate(name = "Task Template 13", description = "Description of Task Template 13", all_or_any = False, choice = "Choice 13", role=role1, process_template = pt1, is_first_task = False)
    tt13.save()
    tt12.children.add(tt13)
    tt12.save()

    tt21 = TaskTemplate(name = "Task Template 21", description = "Description of Task Template 21", all_or_any = False, choice = "Choice 21", role=role1, process_template = pt2, is_first_task = True)
    tt21.save()
    tt22 = TaskTemplate(name = "Task Template 22", description = "Description of Task Template 22", all_or_any = True, choice = "Choice 22", role=role2, process_template = pt2, is_first_task = False)
    tt22.save()
    tt21.children.add(tt22)
    tt21.save()
    tt23 = TaskTemplate(name = "Task Template 23", description = "Description of Task Template 23", all_or_any = False, choice = "Choice 23", role=role1, process_template = pt2, is_first_task = False)
    tt23.save()
    tt22.children.add(tt23)
    tt22.save()
    tt24 = TaskTemplate(name = "Task Template 24", description = "Description of Task Template 24", all_or_any = False, choice = "Choice 24", role=role2, process_template = pt1, is_first_task = False)
    tt24.save()
    tt23.children.add(tt24)
    tt23.save()

    # First Number template, second number iteration
    e11 = Process(name = "Execution 11", template = pt1, creator = actor2, dateOfCreation = datetime.now())
    e11.save()
    deadlinee1 = datetime.now()
    deadlinee1 = deadlinee1.replace(hour=12)
    deadlinee2 = datetime.now()
    deadlinee2 = deadlinee2.replace(second=30)
    et111 = Task(output = "Output of Task 1 Execution 1", deadline = deadlinee1, status = "Started", template = tt11, process = e11)
    et111.save()
    et112 = Task(output = "Output of Task 2 Execution 1", deadline = deadlinee2, status = "Not Started", template = tt12, process = e11)
    et112.save()
    et113 = Task(output = "Output of Task 3 Execution 1", deadline = deadlinee1, status = "Not Started", template = tt13, process = e11)
    et113.save()

    e12 = Process(name = "Execution 12", template = pt1, creator = actor2, dateOfCreation = datetime.now())
    e12.save()
    et121 = Task(output = "Output of Task 1 Execution 2", deadline = deadlinee1, status = "Started", template = tt11, process = e12)
    et121.save()
    et122 = Task(output = "Output of Task 2 Execution 2", deadline = deadlinee2, status = "Not Started", template = tt12, process = e12)
    et122.save()
    et123 = Task(output = "Output of Task 3 Execution 2", deadline = deadlinee1, status = "Not Started", template = tt13, process = e12)
    et123.save()

    e21 = Process(name = "Execution 21", template = pt2, creator = actor1, dateOfCreation = datetime.now())   
    e21.save()
    et211 = Task(output = "Output of Task 1 Execution 1", deadline = deadlinee1, status = "Started", template = tt21, process = e21)
    et211.save()
    et212 = Task(output = "Output of Task 2 Execution 1", deadline = deadlinee2, status = "Not Started", template = tt22, process = e21)
    et212.save()
    et213 = Task(output = "Output of Task 3 Execution 1", deadline = deadlinee1, status = "Not Started", template = tt23, process = e21)
    et213.save()
    et214 = Task(output = "Output of Task 4 Execution 1", deadline = deadlinee1, status = "Not Started", template = tt24, process = e21)
    et214.save()


@login_required
def index(request, exec_id):
    exec_name = "Name of Execution"
    task_list = Task.objects.filter(process_id=exec_id)
    total_action_list = []
    for task in task_list:
        task_template = task.template
        task_template_actions = task_template.status_states
        action_list = parse_csv(task_template_actions)
        total_action_list.append(action_list)
    
    print(total_action_list)
    
    current_user = Actor.objects.filter(name=request.user.get_username())
    # print(Role.objects.filter(actor__id=current_user.get().id))
    user_roles = Role.objects.filter(actor__id=current_user.get().id)
    # print(user_roles)

    template = loader.get_template('view_execution.html')
    collapse_show = "collapse show"
    collapse = "collapse"
    context = {
        'exec_name' : exec_name,
        'task_list' : task_list,
        'user_roles' : user_roles,
        'total_action_list': total_action_list,
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
            out = current_task.get().output + action_user.get().name + ":" + action + ";"
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
