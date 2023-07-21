from django import template

register = template.Library()

@register.filter
def get_file_names(value):
    return ", ".join([f.name for f in value])
