from django.conf.urls import patterns, url
from . import views

SLUG = "(?P<slug>[-_\w]+)"

urlpatterns = [
    # View
    url(r'^'+SLUG+'$', views.page, name='page'),
]
