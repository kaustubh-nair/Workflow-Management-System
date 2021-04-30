from django.contrib.auth.models import User
from ...models.role import Role
from ...models.actor import Actor
from ...models.process_template import ProcessTemplate
from ...models.process import Process
from ...models.task_template import TaskTemplate
from ...models.task import Task

from datetime import datetime

from django.core.management.base import BaseCommand
import random

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        init(self)
        self.stdout.write('done.')

def init(self):

    user = User.objects.create(username="Actor1")
    user.set_password("Actor1Password")
    user.save()
    user = User.objects.create(username="Actor2")
    user.set_password("Actor3Password")
    user.save()
    user = User.objects.create(username="Actor3")
    user.set_password("Actor3Password")
    user.save()

    role1 = Role(name = "Role 1")
    role1.save()
    role2 = Role(name = "Role 2")
    role2.save()
    
    actor1 = Actor(name = "Actor1", group='CU')
    actor1.save()
    actor1.roles.add(role1)
    actor1.save()
    actor2 = Actor(name = "Actor2", group='EU')
    actor2.save()
    actor2.roles.add(role1)
    actor2.roles.add(role2)
    actor2.save()
    actor3 = Actor(name = "Actor3", group='EU')
    actor3.save()
    actor3.roles.add(role2)
    actor3.save()
    
    pt1 = ProcessTemplate(name = "Process Template 1", description = "Description of Process Template 1", creator = actor1, dateOfCreation = datetime.now())
    pt1.save()
    pt2 = ProcessTemplate(name = "Process Template 2", description = "Description of Process Template 2", creator = actor1, dateOfCreation = datetime.now())
    pt2.save()

    tt11 = TaskTemplate(name = "Task Template 11", description = "Description of Task Template 11", all_or_any = False, choice = "Choice 11", role=role1, process_template = pt1, is_first_task = True, status_states= "Approve,Reject")
    tt11.save()
    tt12 = TaskTemplate(name = "Task Template 12", description = "Description of Task Template 12", all_or_any = True, choice = "Choice 12", role=role2, process_template = pt1, is_first_task = False, status_states= "Approve,Reject")
    tt12.save()
    tt11.children.add(tt12)
    tt11.save()
    tt13 = TaskTemplate(name = "Task Template 13", description = "Description of Task Template 13", all_or_any = False, choice = "Choice 13", role=role1, process_template = pt1, is_first_task = False, status_states= "Approve,Reject")
    tt13.save()
    tt12.children.add(tt13)
    tt12.save()

    tt21 = TaskTemplate(name = "Task Template 21", description = "Description of Task Template 21", all_or_any = False, choice = "Choice 21", role=role1, process_template = pt2, is_first_task = True, status_states= "Approve,Reject")
    tt21.save()
    tt22 = TaskTemplate(name = "Task Template 22", description = "Description of Task Template 22", all_or_any = True, choice = "Choice 22", role=role2, process_template = pt2, is_first_task = False, status_states= "Approve,Reject")
    tt22.save()
    tt21.children.add(tt21)
    tt21.save()
    tt23 = TaskTemplate(name = "Task Template 23", description = "Description of Task Template 23", all_or_any = False, choice = "Choice 23", role=role1, process_template = pt2, is_first_task = False, status_states= "Approve,Reject")
    tt23.save()
    tt22.children.add(tt23)
    tt22.save()
    tt24 = TaskTemplate(name = "Task Template 24", description = "Description of Task Template 24", all_or_any = False, choice = "Choice 24", role=role2, process_template = pt1, is_first_task = False, status_states= "Approve,Reject")
    tt24.save()
    tt23.children.add(tt24)
    tt23.save()

    # First Number template, second number iteration
    e11 = Process(name = "Execution 11", template = pt1, creator = actor2, dateOfCreation = datetime.now())
    e11.save()
    deadlinee1 = datetime.now()
    deadlinee1 = deadlinee1.replace(hour=12)
    deadlinee2 = datetime.now()
    deadlinee2 = deadlinee2.replace(second=30)
    et111 = Task(output = "", deadline = deadlinee1, status = "Started", template = tt11, process = e11)
    et111.save()
    et112 = Task(output = "", deadline = deadlinee2, status = "Not Started", template = tt12, process = e11)
    et112.save()
    et113 = Task(output = "", deadline = deadlinee1, status = "Not Started", template = tt13, process = e11)
    et113.save()

    e12 = Process(name = "Execution 12", template = pt1, creator = actor2, dateOfCreation = datetime.now())
    e12.save()
    et121 = Task(output = "", deadline = deadlinee1, status = "Started", template = tt11, process = e12)
    et121.save()
    et122 = Task(output = "", deadline = deadlinee2, status = "Not Started", template = tt12, process = e12)
    et122.save()
    et123 = Task(output = "", deadline = deadlinee1, status = "Not Started", template = tt13, process = e12)
    et123.save()

    e21 = Process(name = "Execution 21", template = pt2, creator = actor1, dateOfCreation = datetime.now())   
    e21.save()
    et211 = Task(output = "", deadline = deadlinee1, status = "Started", template = tt21, process = e21)
    et211.save()
    et212 = Task(output = "", deadline = deadlinee2, status = "Not Started", template = tt22, process = e21)
    et212.save()
    et213 = Task(output = "", deadline = deadlinee1, status = "Not Started", template = tt23, process = e21)
    et213.save()
    et214 = Task(output = "", deadline = deadlinee1, status = "Not Started", template = tt24, process = e21)
    et214.save()

