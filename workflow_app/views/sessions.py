from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.views import generic
from django.urls import reverse_lazy, reverse
from ..models import ProcessTemplate

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
    pt_list = ProcessTemplate.objects.all()
    context = {'pt_list' : pt_list}
    return render(request, 'viewdefinitions.html', context)