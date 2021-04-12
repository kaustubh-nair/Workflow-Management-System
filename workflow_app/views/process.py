from django.shortcuts import render
from datetime import datetime
from django.template import loader
from django.http import HttpResponse

from ..models import ProcessTemplate
from ..models import Task
from .forms import ProcessTemplateForm

def create_template(request):
    tasks = {}

    if request.method == 'POST':
        form = ProcessTemplateForm(request.POST.dict())
        if form.is_valid():
            form.save()
    else:
        tasks = Task.build_tasks(request)
        form = ProcessTemplateForm()

    context = {'form': form, 'tasks': tasks}

    return render(request, 'create_process_template.html', context)
