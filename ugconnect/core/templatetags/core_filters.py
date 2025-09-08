from django import template

register = template.Library()


@register.filter
def split(value, delimiter=','):
    """
    Split a string by a delimiter and return a list.
    Usage: {{ "apple,banana,cherry"|split:"," }}
    """
    if value:
        return [item.strip() for item in str(value).split(delimiter)]
    return []


@register.filter
def join_with_badges(value, css_class="badge bg-info"):
    """
    Join a list or comma-separated string into HTML badges.
    Usage: {{ focus_areas|join_with_badges:"badge bg-primary" }}
    """
    if not value:
        return ""
    
    if isinstance(value, str):
        items = [item.strip() for item in value.split(',') if item.strip()]
    else:
        items = value
    
    badges = []
    for item in items:
        badges.append(f'<span class="{css_class}">{item}</span>')
    
    return ' '.join(badges)


@register.filter
def strip_whitespace(value):
    """
    Strip whitespace from a string.
    Usage: {{ some_string|strip_whitespace }}
    """
    if value:
        return str(value).strip()
    return value
