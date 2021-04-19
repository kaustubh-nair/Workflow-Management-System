from django import forms
from datetime import date

from ..models import Actor, ProcessTemplate, TaskTemplate, Role

class ProcessForm(forms.Form):
    name = forms.CharField(max_length=200, required=False)
    status = forms.ChoiceField(choices=[r.name for r in Role.objects.all()])
