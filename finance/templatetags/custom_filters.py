from django import template
from builtins import abs as builtin_abs  

register = template.Library()


@register.filter
def to(value, arg):
    return range(int(value), int(arg) + 1)


@register.filter(name='absolute')
def absolute(value):
    try:
        return builtin_abs(float(value))
    except (ValueError, TypeError):
        return 0


@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def get_range(start, end):
    return range(start, end)
