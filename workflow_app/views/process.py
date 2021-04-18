from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse

from ..models import ProcessTemplate
from ..models import Role

def index(request):
    role = Role()
    return HttpResponse(role)
