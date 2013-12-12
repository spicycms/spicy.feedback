from django import template

register = template.Library()

@register.filter
def is_set(value, arg):
    return value & arg


@register.filter
def dict_get(value, arg):
    return value.get(arg)
