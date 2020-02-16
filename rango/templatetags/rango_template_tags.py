from django import template
from rango.models import Category

# This new template is used by the Django template engine 
# to render the list of categories you provide in the dictionary
# that is returned in the function.

register = template.Library()

@register.inclusion_tag('rango/categories.html')

# this method returns a dictionary with one key/value pairing
def get_category_list(current_category=None):
    return {'categories': Category.objects.all(), 'current_category': current_category}


