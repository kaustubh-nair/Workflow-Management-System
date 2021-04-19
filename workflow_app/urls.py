from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
        # path('process/template/create/', views.process_template.create_template, name='create_process_template'),
        path('', views.sessions.home, name='home'),
        path('viewdefs', views.sessions.viewdefs, name = 'viewdefs'),
        path('accounts/signup', views.sessions.SignUpView.as_view(), name='signup'),
        path('process/create/', views.process.create, name='create_process'),
        path('viewexec/<int:exec_id>/', views.execution.index, name='executionindex'),
        path('viewexec/<int:exec_id>/completetask/<int:task_id>/', views.execution.completeTask, name='completing task')
]
