from django.urls import path

from . import views

urlpatterns = [
        path('', views.process.index, name='index'),
        path('execindex', views.execution.index, name='executionindex'),
]
