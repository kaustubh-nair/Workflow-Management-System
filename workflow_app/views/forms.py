from django import forms

from ..models import ProcessTemplate

class ProcessTemplateForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=1000)
