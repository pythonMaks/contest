from django import template

register = template.Library()

@register.filter
def average(value_list):
    return round((sum(value_list) / len(value_list)), 2) if value_list else 0

