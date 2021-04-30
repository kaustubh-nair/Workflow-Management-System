from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    group_choices = ('CU', 'Creation User'), ('EU', 'Execution User')
    group_field = forms.CharField(label='User Type', widget=forms.RadioSelect(choices=group_choices))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'group_field', )
