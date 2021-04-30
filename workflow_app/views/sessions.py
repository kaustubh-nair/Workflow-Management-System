from django.contrib.auth import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.views import generic
from django.urls import reverse_lazy, reverse
from ..models import ProcessTemplate, Process, Actor, Role, TaskTemplate, Task
from .signup_form import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            group = form.cleaned_data.get('group_field')
            if not Actor.objects.filter(name=username):
                temp = Actor(name=username, group=group)
                temp.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('viewdefs', args=(request.user.username, )))
    else:
        return HttpResponseRedirect(reverse('login'))

def viewdefs(request, name):
    curr_actor = Actor.objects.get(name=name)
    def_list = ProcessTemplate.objects.all().order_by('-dateOfCreation')
    context = {'def_list' : def_list, 'group' : curr_actor.group}
    return render(request, 'viewdefinitions.html', context)

def viewexecs(request, name, def_id):
    exec_list = Process.objects.filter(template__id = def_id)
    process_template = ProcessTemplate.objects.filter(id = def_id).get()
    print(process_template.id)
    context = {
        'process_template' : process_template,
        'exec_list' : exec_list
        }
    return render(request, 'viewexecutions.html', context)

def viewactors(request, name):
    actor_list = Actor.objects.all()
    role_list = Role.objects.all()
    context = {'actor_list' : actor_list, 'role_list' : role_list}
    return render(request, 'viewactors.html', context)

def add_role_to_actor(request, name, roleid, actorid):
    curr_actor = Actor.objects.get(id=actorid)
    curr_role = Role.objects.get(id=roleid)
    curr_actor.roles.add(curr_role)
    curr_actor.save()
    return HttpResponseRedirect(reverse('viewactors', args=(name,)), request)

def remove_role_from_actor(request, name, roleid, actorid):
    curr_actor = Actor.objects.get(id=actorid)
    curr_role = Role.objects.get(id=roleid)
    curr_actor.roles.remove(curr_role)
    curr_actor.save()
    return HttpResponseRedirect(reverse('viewactors', args=(name,)), request)

# def myexecutions(request, name):
#     exec_list = Process.objects.all()
#     pending_execs = []
#     available_execs = []
#     for e in exec_list:
#         all_templates = TaskTemplate.objects.filter(process_template=e.template)
#         flag = 0
#         for template in all_templates:
#             if template.role in Actor.objects.get(name=name).roles.all():
#                 all_tasks = Task.objects.filter(template=template)
#                 for task in all_tasks:
#                     if flag:
#                         break
#                     if task.status == "Started":
#                         pending_execs.append(e)
#                         flag = 1
#                 if not flag:
#                     available_execs.append(e)
#                     flag = 1
#             if flag:
#                 break
#     context = {
#         'pending_execs' : pending_execs,
#         'available_execs' : available_execs,
#         }
#     return render(request, 'view_my_executions.html', context)

def myexecutions(request, name):
    pending_execs = []
    available_execs = []
    all_process_templates = ProcessTemplate.objects.all()
    for ptemp in all_process_templates:
        all_task_templates = TaskTemplate.objects.filter(process_template=ptemp)
        flag_outer = 0
        for ttemp in all_task_templates:
            if ttemp.role in Actor.objects.get(name=name).roles.all():
                flag_outer = 1
                break
        print(flag_outer)
        if flag_outer:
            flag_inner = 0
            all_processes = Process.objects.filter(template=ptemp)
            for process in all_processes:
                all_tasks = Task.objects.filter(process=process)
                for task in all_tasks:
                    if task.status == "Started" and task.template.role in Actor.objects.get(name=name).roles.all():
                        pending_execs.append(process)
                        flag_inner = 1
                if not flag_inner:
                    available_execs.append(process)
                    flag_inner = 1
                if flag_inner:
                    break
    context = {
        'pending_execs' : pending_execs,
        'available_execs' : available_execs,
        }
    return render(request, 'view_my_executions.html', context)

def index(request, exec_id):
    return HttpResponse("Hi")
