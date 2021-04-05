from django import forms

class SomeForm(forms.Form):
    your_name = forms.CharField(max_length=100)
