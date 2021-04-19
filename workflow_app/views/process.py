from django.shortcuts import render
from datetime import datetime

from ..models import ProcessTemplate, TaskTemplate, Role, Task, Process
from .process_form import ProcessForm

def create(request):
    messages=[]
    form = ProcessForm()
    context = {}
    process_template_id=0
    task_templates = []
    template = ''

    if request.method == 'POST':
        req = dict(request.POST)
        process_id = Process.save_process(req)
        Task.save_tasks(req, process_id)
        messages.append({'type': 'success', 'message': 'Process created successfully'})
    else:
        request_body = dict(request.GET)
        process_template_id = request_body['id'][0]
        template = ProcessTemplate.objects.get(pk=process_template_id).name
        task_templates = [o.__dict__ for o in list(TaskTemplate.objects.all().filter(process_template_id=process_template_id))]
        for i in range(len(task_templates)):
            task_templates[i]['role'] = Role.objects.get(pk=task_templates[i]['role_id']).name

    context.update({'form': form, 'messages': messages, 'task_templates': task_templates, 'template': template, 'process_template_id': process_template_id})
    return render(request, 'create_process.html', context)
