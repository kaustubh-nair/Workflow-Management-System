from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
        path('', views.sessions.home, name='home'),
        path('<str:name>/viewdefs', views.sessions.viewdefs, name = 'viewdefs'),
        path('<str:name>/viewexecs/<int:def_id>', views.sessions.viewexecs, name = 'viewexecs'),
        path('<str:name>/viewactors', views.sessions.viewactors, name = 'viewactors'),
        path('<str:name>/createrole', views.sessions.create_role, name = 'create_role'),
        path('<str:name>/deleterole', views.sessions.delete_role, name = 'delete_role'),
        path('<str:name>/addrole/<int:roleid>/toactor/<int:actorid>', views.sessions.add_role_to_actor, name = 'add_role_to_actor'),
        path('<str:name>/removerole/<int:roleid>/fromactor/<int:actorid>', views.sessions.remove_role_from_actor, name = 'remove_role_from_actor'),
        path('<str:name>/myexecutions', views.sessions.myexecutions, name = 'myexecutions'),
        path('process/template/create/', views.process.create_template, name='create_process_template'),
        path('process/<int:process_template_id>/task/add/', views.process.add_task, name='add_task'),
        path('process/<int:template_id>/create/', views.process.create, name='create_process'),
        path('task/<int:process_template_id>/<int:task_id>/up/', views.process.move_task_up, name='task_up'),
        path('task/<int:process_template_id>/<int:task_id>/down/', views.process.move_task_down, name='task_down'),
        path('process/template/<int:process_id>/edit/', views.process.edit, name='edit_process_template'),
        path('task/template/<int:task_template_id>/edit/', views.process.edit_task, name='edit_process'),
        path('create/exec/<int:template_id>', views.execution.create_exec, name='create_execution'),
        path('change/execname/<int:execution_id>', views.execution.change_exec_name, name='changeexecname'),
        path('change/deadline/<int:execution_id>/<int:task_id>', views.execution.change_deadline, name='changedeadline'),
        path('resetfrom/<int:execution_id>/<int:task_id>',views.execution.reset_from, name='reset_from'),
        path('delete/exec/<int:execution_id>', views.execution.delete_exec, name='delete_execution'),
        path('viewexec/<int:exec_id>/', views.execution.index, name='executionindex'),
        path('viewexec/<int:exec_id>/completetask/<int:task_id>/<str:action>', views.execution.completeTask, name='completing task'),
        path('accounts/signup', views.sessions.signup, name='signup'),
]
