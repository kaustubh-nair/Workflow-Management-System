from django.contrib import admin

from django.apps import apps

for _, model in apps.get_app_config('workflow_app').models.items():
    admin.site.register(model)
