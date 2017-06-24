from django import  template
from django.utils.safestring import mark_safe



register=template.Library()


@register.simple_tag
def redner_paginator_btn(articles,page):
    current_page = articles.number
    if abs(current_page - page) < 2:
        ele="""<li class=""><a href="?page={ page }">{ page }<span class="sr-only"></span></a></li>""".format(page=page)
        return mark_safe(ele)
    return ''