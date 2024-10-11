from django import template

register = template.Library()

@register.filter
def range_(count):
    """Return a range of numbers from 0 to count - 1."""
    return range(count)
