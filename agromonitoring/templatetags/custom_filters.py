from django import template

register = template.Library()

@register.filter
def kelvin_to_celsius(value):
    return value - 273.15
