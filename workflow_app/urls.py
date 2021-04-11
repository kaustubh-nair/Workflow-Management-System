from django.urls import path

from . import views

urlpatterns = [
        path('process/template/create/', views.process.create_template, name='create_process_template'),
        path('', views.process.index, name='index'),
        path('execindex/<int:task_id>/', views.execution.index, name='executionindex'),
]
