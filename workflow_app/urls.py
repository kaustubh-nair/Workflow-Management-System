from django.urls import path

from . import views

urlpatterns = [
        path('process/template/create/', views.process_template.create_template, name='create_process_template'),
]
