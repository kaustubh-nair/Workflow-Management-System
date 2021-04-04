from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse

from .models import Role

def index(request):
    role = Role()
    return HttpResponse(role)
