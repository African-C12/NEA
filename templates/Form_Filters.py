from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(field, css_class):
    return field.as_widget(attrs={'class': css_class})

@register.filter(name='addtype')
def addtype(field, field_type):
    return field.as_widget(attrs={'type': field_type})