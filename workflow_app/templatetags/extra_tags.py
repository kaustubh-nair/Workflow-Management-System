from django import template

register = template.Library()

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.filter
def humanreadable(text):
    return text.replace('_', ' ').capitalize()

@register.filter
def parse_csv(text):
    return [ x.strip() for x in text.split(',')]

@register.filter
def get_task_edit_url(id):
    return "/task/template/" + str(id) + "/edit"

@register.filter
def get_process_edit_url(id):
    return "/process/template/" + str(id) + "/edit"

@register.filter
def get_add_new_task_url(id):
    return "/process/" + str(id) + "/task/add/"

