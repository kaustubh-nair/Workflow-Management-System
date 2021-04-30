from django import forms
from datetime import date

from ..models import Actor, ProcessTemplate, TaskTemplate, Role

class EditProcessTemplateForm(forms.Form):
    name = forms.CharField(max_length=200, required=False)
    description = forms.CharField(max_length=1000, required=False)

class ProcessTemplateForm(forms.Form):
    name = forms.CharField(max_length=200, required=False)
    description = forms.CharField(max_length=1000, required=False)

    new_task_name = forms.CharField(max_length=200, required=False)
    new_task_description = forms.CharField(max_length=1000, required=False)
    new_task_all_or_any = forms.BooleanField(required=False)
    #new_task_choice = forms.CharField(max_length=200)
    new_task_role = forms.ChoiceField(choices=[r.name for r in Role.objects.all()])
    new_task_status_states = forms.CharField(max_length=3000, required=False)

    def __init__(self, request=None):
        if not request:
            return super().__init__()

        tasks = {}
        # Tasks are defined in form numberlabel
        for k, v in request.items():
            if k[0].isdigit():
                number = TaskTemplate.get_task_number_from_param(k)
                label = [k[1:] if not k[1].isdigit() else k[2:]][0]
                if number not in tasks:
                    tasks[number] = {}

                tasks[number][label] = v

        self.tasks = tasks
        self.name = request['name']
        self.description = request['description']

        return super().__init__(request)

    def save(self):
        process_template = ProcessTemplate.objects.create(name=self.name, description=self.description, creator=Actor.objects.first(), dateOfCreation=date.today())
        for number, task in self.tasks.items():
                print(number)
                TaskTemplate.objects.create(name=task['name'], description=task['description'], role_id=1, process_template_id=process_template.id, status_states=task['status_states'])
