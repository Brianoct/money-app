from django import template

register = template.Library()

@register.filter
def format_for_css(value):
    """
    Format a number for use in CSS (e.g., ensure decimal separator is a dot).
    """
    try:
        return f"{float(value):.1f}"  # Format as a float with 1 decimal place (e.g., 75.5)
    except (ValueError, TypeError):
        return "0"  # Fallback to 0 if the value is invalid