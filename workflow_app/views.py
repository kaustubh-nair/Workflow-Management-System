from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from . import models

def index(request):
    return HttpResponse("asd")
