from django import forms

from ..models import ProcessTemplate, TaskTemplate

class ProcessTemplateForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=1000)

    new_task_name = forms.CharField(max_length=200)
    new_task_description = forms.CharField(max_length=1000)
    new_task_all_or_any = forms.BooleanField()
    new_task_choice = forms.CharField(max_length=200)
    new_task_role = forms.CharField(max_length=200)

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
        ProcessTemplate.objects.create(name=self.name, description=self.description, creator_id=1)
