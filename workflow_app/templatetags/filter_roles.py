from django import template
from ..models import Role, Actor

register = template.Library()

@register.filter
def filter_absent(all_roles, actorid):
    actor_roles = Actor.objects.get(id=actorid).roles
    not_actor_roles = []
    for role in all_roles:
        if role not in actor_roles.all():
            not_actor_roles.append(role)
    return not_actor_roles