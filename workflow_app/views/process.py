from django.shortcuts import render, redirect
from django.template import loader
from datetime import datetime
from ..models import ProcessTemplate, TaskTemplate, Role, Task, Process
from .process_form import ProcessForm
from .process_template_form import ProcessTemplateForm, EditProcessTemplateForm
from .task_template_form import TaskTemplateForm

def add_task(request, process_template_id):
    messages=[]
    process_template = ProcessTemplate.objects.filter(id=process_template_id).first()
    if request.method == 'POST':
        req = dict(request.POST)
        TaskTemplate.objects.create(name=req['name'][0], description= req['description'][0], all_or_any=[True if 'all_or_any' in req else False][0], status_states=req['status_states'][0], role_id=int(req['role'][0]), process_template=process_template)
        messages.append({'type': 'success', 'message': 'Task added successfully'})

    form = TaskTemplateForm()
    context = {'process_template_id': process_template_id, 'form': form, 'messages': messages}
    return render(request, 'add_task_template.html', context)

def edit(request, process_id):
    messages=[]
    process_template = ProcessTemplate.objects.filter(id=process_id).first()
    if request.method == 'POST':
        req = dict(request.POST)
        process_template.name = req['name'][0]
        process_template.description = req['description'][0]
        process_template.save()
        messages.append({'type': 'success', 'message': 'Workflow edited successfully'})
    form = EditProcessTemplateForm(initial={'name': process_template.name, 'description': process_template.description})
    task_templates = TaskTemplate.objects.filter(process_template=process_template)
    task_templates = [(t.id, t.name) for t in task_templates]
    context = {'messages': messages, 'process_template_id': process_template.id, 'form': form, 'tasks': task_templates}

    return render(request, 'edit_process_template.html', context)

def edit_task(request, task_template_id):
    messages=[]
    task_template = TaskTemplate.objects.filter(id=task_template_id).first()
    if request.method == 'POST':
        req = dict(request.POST)
        task_template.name = req['name'][0]
        task_template.description = req['description'][0]
        task_template.all_or_any = [True if 'all_or_any' in req else False][0]
        task_template.status_states = req['status_states'][0]
        task_template.role_id = int(req['role'][0])
        task_template.save()

    role = task_template.role
    role=(role.id, role.name)
    form = TaskTemplateForm(initial={'name': task_template.name, 'all_or_any': task_template.all_or_any, 'role': role, 'description': task_template.description, 'status_states': task_template.status_states })
    context = {'id': task_template.process_template_id, 'form': form, 'messages': messages}
    return render(request, 'edit_task_template.html', context)

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
        messages.append({'type': 'success', 'message': 'Workflow created successfully'})
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
            return redirect('/', messages=messages)
    else:
        tasks = TaskTemplate.build_tasks(dict(request.GET))

    context = {'form': form, 'tasks': tasks, 'messages': messages}

    return render(request, 'create_process_template.html', context)
