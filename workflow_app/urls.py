from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
        path('', views.sessions.home, name='home'),
        path('<str:name>/viewdefs', views.sessions.viewdefs, name = 'viewdefs'),
        path('viewexecs/<int:def_id>', views.sessions.viewexecs, name = 'viewexecs'),
        path('process/template/create/', views.process.create_template, name='create_process_template'),
        path('process/<int:process_template_id>/task/add/', views.process.add_task, name='add_task'),
        path('process/create/', views.process.create, name='create_process'),
        path('process/template/<int:process_id>/edit/', views.process.edit, name='edit_process_template'),
        path('task/template/<int:task_template_id>/edit/', views.process.edit_task, name='edit_process'),
        path('viewexec/<int:exec_id>/', views.execution.index, name='executionindex'),
        path('viewexec/<int:exec_id>/completetask/<int:task_id>/<str:action>', views.execution.completeTask, name='completing task'),
        path('accounts/signup', views.sessions.signup, name='signup'),
]
