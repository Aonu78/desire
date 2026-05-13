from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    """Replace occurrences of one string with another.

    Usage: {{ value|replace:"-|| " }}
    """
    try:
        old, new = arg.split('||', 1)
    except ValueError:
        return value
    return value.replace(old, new)
