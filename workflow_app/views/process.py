from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse

from ..models import ProcessTemplate
from .forms import SomeForm

def index(request):
    return render(request, 'create_process.html', {'form': SomeForm()})
