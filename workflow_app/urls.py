from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
        path('', views.sessions.home, name='home'),
        path('viewdefs', views.sessions.viewdefs, name = 'viewdefs'),
        path('viewexecs/<int:def_id>', views.sessions.viewexecs, name = 'viewexecs'),
        path('accounts/signup', views.sessions.SignUpView.as_view(), name='signup'),
        path('process/template/create/', views.process.create_template, name='create_process_template'),
        path('process/create/', views.process.create, name='create_process'),
        path('create/exec/<int:template_id>', views.execution.create_exec, name='create_execution'),
        path('viewexec/<int:exec_id>/', views.execution.index, name='executionindex'),
        path('viewexec/<int:exec_id>/completetask/<int:task_id>/<str:action>', views.execution.completeTask, name='completing task')
]
