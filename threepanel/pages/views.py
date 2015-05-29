from dashboard.views import render
from django.template.loader import TemplateDoesNotExist
from django.http import Http404
from slugify import slugify

# Create your views here.
def page(request, slug):
    # this is redundant but I just want to make sure
    slug = slugify(slug)

    try:
        return render(request, "pages/"+slug+".html")
    except TemplateDoesNotExist:
        raise Http404("Page not found!")

