from django import  template
from django.utils.safestring import mark_safe



register=template.Library()


@register.simple_tag
def paging(a):
    print('a1',a)
    return a