from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(field, css_class):
    """Add a CSS class to the specified form field."""
    return field.as_widget(attrs={'class': css_class})

@register.filter(name='addtype')
def addtype(field, field_type):
    """Add an input type to the specified form field."""
    return field.as_widget(attrs={'type': field_type})