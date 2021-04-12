from django.shortcuts import render
from datetime import datetime

from ..models import ProcessTemplate, TaskTemplate

def create(request):
    messages=[]

    context = {'messages': messages}
    return render(request, 'create_process.html', context)
