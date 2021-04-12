from django.urls import path

from . import views

urlpatterns = [
        path('process/template/create/', views.process.create_template, name='create_process_template'),
        # path('', views.process.index, name='index'),
        path('viewexec/<int:exec_id>/', views.execution.index, name='executionindex'),
        path('viewexec/<int:exec_id>/completetask/<int:task_id>/', views.execution.completeTask, name='completing task')
]
