from django.contrib.auth import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from ..models import ProcessTemplate, Process, Actor, Role, TaskTemplate, Task
from .signup_form import SignUpForm

def signup(request):
    messages = []
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
            messages.append(form.errors)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'messages': messages})

def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('viewdefs', args=(request.user.username, )))
    else:
        return HttpResponseRedirect(reverse('login'))

@login_required
def viewdefs(request, name):
    curr_actor = Actor.objects.get(name=name)
    def_list = ProcessTemplate.objects.all().order_by('-dateOfCreation')
    context = {'def_list' : def_list, 'group' : curr_actor.group}
    return render(request, 'viewdefinitions.html', context)

@login_required
def viewexecs(request, name, def_id):
    exec_list = Process.objects.filter(template__id = def_id)
    process_template = ProcessTemplate.objects.filter(id = def_id).get()
    print(process_template.id)
    context = {
        'process_template' : process_template,
        'exec_list' : exec_list
        }
    return render(request, 'viewexecutions.html', context)

@login_required
def viewactors(request, name):
    actor_list = Actor.objects.all()
    role_list = Role.objects.all()
    dup_message = ""
    inv_message = ""
    context = {'actor_list' : actor_list, 'role_list' : role_list, 'dup_message' : dup_message, 'inv_message' : inv_message}
    return render(request, 'viewactors.html', context)

@login_required
def create_role(request, name):
    rolename = request.POST.get('rolename')
    role_list = Role.objects.all()
    present = 0
    for role in role_list:
        if role.name == rolename:
            present = 1
            break
    if not present:
        new_role = Role(name=rolename)
        new_role.save()
        return HttpResponseRedirect(reverse('viewactors', args=(name,)), request)
    else:
        actor_list = Actor.objects.all()
        dup_message = "Duplicate role name. Please enter a unique name"
        inv_message = ""
        context = {'actor_list' : actor_list, 'role_list' : role_list, 'dup_message' : dup_message, 'inv_message' : inv_message}
        return render(request, 'viewactors.html', context)

@login_required
def delete_role(request, name):
    deleterolename = request.POST.get('deleterolename')
    role_list = Role.objects.all()
    present = 0
    for role in role_list:
        if role.name == deleterolename:
            present = 1
            break
    if present:
        curr_role = Role.objects.get(name=deleterolename)
        curr_role.delete()
        return HttpResponseRedirect(reverse('viewactors', args=(name,)), request)
    else:
        actor_list = Actor.objects.all()
        dup_message = ""
        inv_message = "Role does not exist. Please enter a valid name"
        context = {'actor_list' : actor_list, 'role_list' : role_list, 'dup_message' : dup_message, 'inv_message' : inv_message}
        return render(request, 'viewactors.html', context)

@login_required
def add_role_to_actor(request, name, roleid, actorid):
    curr_actor = Actor.objects.get(id=actorid)
    curr_role = Role.objects.get(id=roleid)
    curr_actor.roles.add(curr_role)
    curr_actor.save()
    return HttpResponseRedirect(reverse('viewactors', args=(name,)), request)

@login_required
def remove_role_from_actor(request, name, roleid, actorid):
    curr_actor = Actor.objects.get(id=actorid)
    curr_role = Role.objects.get(id=roleid)
    curr_actor.roles.remove(curr_role)
    curr_actor.save()
    return HttpResponseRedirect(reverse('viewactors', args=(name,)), request)

@login_required
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
        if flag_outer:
            flag_inner = 0
            all_processes = Process.objects.filter(template=ptemp)
            for process in all_processes:
                all_tasks = Task.objects.filter(process=process)
                for task in all_tasks:
                    r = Actor.objects.get(name=name).roles.all()
                    if task.status == "Started" and task.template.role in r:
                        pending_execs.append(process)
                        flag_inner = 1
                if not flag_inner:
                    available_execs.append(process)
                
    context = {
        'pending_execs' : pending_execs,
        'available_execs' : available_execs,
        }
    return render(request, 'view_my_executions.html', context)

def index(request):
    return HttpResponse("Hi")
