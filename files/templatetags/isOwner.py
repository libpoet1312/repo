from django import template
from django.shortcuts import get_object_or_404

register = template.Library()


@register.filter(name="isOwner")
def isOwner(user, file):
    print(file)
    print(user == file.uploader)
    if file.uploader == user:
        return True
    else:
        return False
