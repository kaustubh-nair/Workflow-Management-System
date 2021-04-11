from django import forms

from ..models import ProcessTemplate

class ProcessTemplateForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=1000)

    task_name = forms.CharField(max_length=200)
    task_description = forms.CharField(max_length=1000)
    task_all_or_any = forms.BooleanField()
    task_choice = forms.CharField(max_length=200)
    task_role = forms.CharField(max_length=200)
