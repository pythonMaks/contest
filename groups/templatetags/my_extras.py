from django import template

register = template.Library()

@register.filter
def average(value_list):
    return sum(value_list) / len(value_list) if value_list else 0
