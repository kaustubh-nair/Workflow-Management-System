from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from . import models

def index(request):
    pa = models.ProcessTemplate.objects.create(name="Paper review")
    process = models.Process.objects.create(name="Paper review IIITB", template=pa)

    ta = models.TaskTemplate.objects.create(name="Initialize", all_or_any=False)
    tb = models.TaskTemplate.objects.create(name="Review", all_or_any=False)
    tc = models.TaskTemplate.objects.create(name="Accept/Reject", all_or_any=False)
    seqa = models.TaskSequence.objects.create(parent=ta, child=tb)
    seqb = models.TaskSequence.objects.create(parent=tb, child=tc)


    ra = models.Role.objects.create(name="rolea")
    rb = models.Role.objects.create(name="roleb")
    rc = models.Role.objects.create(name="rolec")
    actor = models.Actor.objects.create(name="boo")
    actor.roles.add(ra)
    actor.roles.add(rc)
    actor.save()
    actor2 = models.Actor.objects.create(name="brahma")
    actor2.roles.add(ra)
    actor2.roles.add(rb)
    actor2.save()


    tasks = []
    t = [ta, tb, tc]
    for i in range(3):
        task = models.Task.objects.create(output="output" + str(i),deadline=datetime.now(), template=t[i], process=process, status="Incomplete")
        tasks.append(task)

    tasks[0].status = "Ongoing"  # Add constraints for permissible values.
    tasks[0].save()

    tasks[1].status = "Ongoing"
    tasks[1].save()

    tasks[2].status = "Ongoing"
    tasks[2].save()

    tasks[0].status = "Complete"
    tasks[0].actors.add(actor)  # Add constraint for role
    tasks[0].save()

    tasks[1].status = "Complete"
    tasks[1].actors.add(actor)
    tasks[1].save()

    tasks[2].status = "Complete"
    tasks[2].actors.add(actor2)
    tasks[2].save()

    return HttpResponse(tasks[1].status)
