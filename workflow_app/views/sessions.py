from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.views import generic
from django.urls import reverse_lazy, reverse
from ..models import ProcessTemplate, Process

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('viewdefs'))
    else:
        return HttpResponseRedirect(reverse('login'))

def viewdefs(request):
    def_list = ProcessTemplate.objects.all()
    context = {'def_list' : def_list}
    return render(request, 'viewdefinitions.html', context)

def viewexecs(request, def_id):
    exec_list = Process.objects.filter(template__id = def_id)
    context = {'exec_list' : exec_list}
    return render(request, 'viewexecutions.html', context)

def index(request, exec_id):
    return HttpResponse("Hi")
