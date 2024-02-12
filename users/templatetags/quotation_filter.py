from django import template
from users.models import Quotation
register= template.Library()


@register.filter
def quotations(arg, value):
    return Quotation.objects.filter(name_of_raw_material=value)

    
