from django.shortcuts import render
from datetime import datetime
from django.template import loader
from django.http import HttpResponse

from ..models import ProcessTemplate, TaskTemplate
from .forms import ProcessTemplateForm

def create_template(request):
    tasks = {}
    form = ProcessTemplateForm()
    messages = []

    if request.method == 'POST':
        request_body = dict(request.POST)
        form = ProcessTemplateForm(request.POST.dict())
        tasks = TaskTemplate.build_tasks(request_body)
        if request_body['action'][0] == 'add_task':
            tasks = TaskTemplate.add_new_task(tasks, request_body)
        elif request_body['action'][0] == 'save':
            # if form.is_valid():
            form.save()
            form = ProcessTemplateForm()
            tasks = {}
            messages.append({'type': 'success', 'message': 'Process template created successfully'})
    else:
        tasks = TaskTemplate.build_tasks(dict(request.GET))

    context = {'form': form, 'tasks': tasks, 'messages': messages}

    return render(request, 'create_process_template.html', context)
