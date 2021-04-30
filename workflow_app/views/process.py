from django.shortcuts import render
from django.template import loader
from datetime import datetime
from ..models import ProcessTemplate, TaskTemplate, Role, Task, Process
from .process_form import ProcessForm
from .process_template_form import ProcessTemplateForm

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
