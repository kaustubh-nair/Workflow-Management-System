from django.shortcuts import render
from datetime import datetime
from django.template import loader
from django.http import HttpResponse

from ..models import ProcessTemplate

def create_template(request):
    context = {'process_template': process_template}
    return render(request, 'create_process.html', context)
