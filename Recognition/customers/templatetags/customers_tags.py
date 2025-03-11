from django import template
from django.utils.http import urlencode


register = template.Library()


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    try:
        query = context['request'].GET.dict()
        query.update(kwargs)
        return urlencode(query)
    except Exception:
        return urlencode(context)


@register.filter(is_safe=False)
def sub(value, arg):
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        try:
            return value - arg
        except Exception:
            return ""
