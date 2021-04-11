from django.shortcuts import render
from datetime import datetime
from django.template import loader
from django.http import HttpResponse

from ..models import ProcessTemplate
from .forms import ProcessTemplateForm

def create_template(request):
    if request.method == 'POST':
        form = ProcessTemplateForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ProcessTemplateForm()

    context = {'form': form}
    return render(request, 'create_process_template.html', context)
