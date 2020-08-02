from django import template

register = template.Library()


@register.filter(name='loadAncestors')
def loadAncestors(instance):
    qs = instance.get_ancestors(include_self=True)
    res = qs.values_list('name', flat=True)
    ret = []
    str = ''
    for re in res:
        ret.append(re)
        str = '/'.join(re)


    return str
