from django import template
from ..models import File
from taggit.models import Tag

register = template.Library()


@register.tag()
def get_tags(self, context):
    tags = File.tags.all()
    print(tags)
    return tags
