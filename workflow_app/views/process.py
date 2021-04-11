from django.shortcuts import render
from datetime import datetime
from django.template import loader
from django.http import HttpResponse

from ..models import ProcessTemplate
from .forms import ProcessTemplateForm

def create_template(request):
    tasks = {}
    if request.method == 'POST':
        form = ProcessTemplateForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        for k,v in dict(request.GET).items():
            if (k.startswith('task')):
                task_number = int(k[4:6])

                if task_number not in tasks:
                    tasks[task_number] = {}

                keyword = k[6:]
                if keyword == 'name':
                    tasks[task_number]['name'] = v[0]
                elif keyword == 'description':
                    tasks[task_number]['description'] = v[0]
                elif keyword == 'all_or_any':
                    tasks[task_number]['all_or_any'] = v[0]
                elif keyword == 'choice':
                    tasks[task_number]['choice'] = v[0]
                elif keyword == 'role':
                    tasks[task_number]['role'] = v[0]


        form = ProcessTemplateForm()

    print(tasks)
    context = {'form': form, 'tasks': tasks}

    return render(request, 'create_process_template.html', context)
