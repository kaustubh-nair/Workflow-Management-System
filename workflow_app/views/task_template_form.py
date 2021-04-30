from django import forms
from ..models import Actor, ProcessTemplate, TaskTemplate, Role

class TaskTemplateForm(forms.Form):
    name = forms.CharField(max_length=200, required=False)
    description = forms.CharField(max_length=1000, required=False)
    all_or_any = forms.BooleanField(required=False)
    role = forms.ChoiceField(choices=[(r.id, r.name) for r in Role.objects.all()])
    status_states = forms.CharField(max_length=3000, required=False)
