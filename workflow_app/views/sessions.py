from django.contrib.auth import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.views import generic
from django.urls import reverse_lazy, reverse
from ..models import ProcessTemplate, Process, Actor
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
    def_list = ProcessTemplate.objects.all()
    context = {'def_list' : def_list, 'group' : curr_actor.group}
    return render(request, 'viewdefinitions.html', context)

def viewexecs(request, def_id):
    exec_list = Process.objects.filter(template__id = def_id)
    context = {'exec_list' : exec_list}
    return render(request, 'viewexecutions.html', context)

def index(request, exec_id):
    return HttpResponse("Hi")
