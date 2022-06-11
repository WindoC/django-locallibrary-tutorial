from django import template
from django.core.paginator import Paginator

register = template.Library()

import sys

@register.simple_tag
def get_proper_elided_page_range(paginator, number, on_each_side=2, on_ends=1):

    number = paginator.validate_number(number)

    extra_on_each_side = 0
    mustdisplay = 1 + on_each_side + 1 + on_ends

    if number < mustdisplay:
        extra_on_each_side = mustdisplay - number
    if paginator.num_pages - number + 1 < mustdisplay:
        extra_on_each_side = mustdisplay - (paginator.num_pages - number + 1)
    # print(extra_on_each_side, file=sys.stderr)

    if paginator.num_pages <= (on_each_side + on_ends) * 2 + extra_on_each_side:
        yield from paginator.page_range
        return

    if number > (1 + on_each_side + extra_on_each_side + on_ends) + 1:
        yield from range(1, on_ends + 1)
        yield paginator.ELLIPSIS
        yield from range(number - on_each_side - extra_on_each_side, number + 1)
    else:
        yield from range(1, number + 1)

    if number < (paginator.num_pages - on_each_side - extra_on_each_side - on_ends) - 1:
        yield from range(number + 1, number + on_each_side + extra_on_each_side + 1)
        yield paginator.ELLIPSIS
        yield from range(paginator.num_pages - on_ends + 1, paginator.num_pages + 1)
    else:
        yield from range(number + 1, paginator.num_pages + 1)