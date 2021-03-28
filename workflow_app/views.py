from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from . import models

def index(request):
    # 
    ta = models.TaskTemplate.objects.create(name="taska", all_or_any=False)
    tb = models.TaskTemplate.objects.create(name="taskb", all_or_any=False)
    tc = models.TaskTemplate.objects.create(name="taskc", all_or_any=False)
    ra = models.Role.objects.create(name="rolea")
    rb = models.Role.objects.create(name="roleb")
    rc = models.Role.objects.create(name="rolec")
    pa = models.ProcessTemplate.objects.create(name="processa")
    actor = models.Actor.objects.create(name="boo")
    actor.roles.add(ra)
    actor.roles.add(rc)
    actor.save()
    actor2 = models.Actor.objects.create(name="brahma")
    actor2.roles.add(ra)
    actor2.roles.add(rb)
    actor2.save()
    process = models.Process.objects.create(name="fuc", template=pa)


    tasks = []
    t = [ta, tb, tc]
    a = [actor, actor, actor2]
    for i in range(3):
        task = models.Task.objects.create(output="ASD" + str(i),deadline=datetime.now(), template=t[i], process=process)
        task.actors.add(a[i])
        task.save()
        tasks.append(task)

    return HttpResponse(tasks[1].template.name)
