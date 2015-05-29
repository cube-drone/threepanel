from django import template
from django.utils.safestring import mark_safe
from slugify import slugify

register = template.Library()

@register.filter
def highlight(value, arg):
    if not arg:
        return value
    slargs = []
    for item in arg.split(" "):
        slargs.append(slugify(item))
    lst = value.split(" ")
    new_lst = []
    for item in lst:
        if slugify(item) in slargs:
            new_lst.append("<strong class='result'>{}</strong>".format(item))
        else:
            new_lst.append(item)
    return mark_safe(" ".join(new_lst))
