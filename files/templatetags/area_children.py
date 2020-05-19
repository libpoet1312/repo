from django import template
from django.shortcuts import get_object_or_404
from ..models import Area

register = template.Library()


@register.filter()
def get_children(area):
    obj = get_object_or_404(Area, name=area)
    children = obj.get_children()
    print(children)
    return ',\n'.join([x['name'] for x in children.values()])


@register.filter()
def get_skata(area):
    return area
