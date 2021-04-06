from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse

from ..models import Role
from ..models import Task

def index(request):
    role = Task()
    return HttpResponse(role)

