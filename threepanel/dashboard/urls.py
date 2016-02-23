from django.conf.urls import patterns, url
from . import views

SITE_SLUG = "(?P<site_slug>[-_\w]+)"

urlpatterns = patterns('',
    url(r'^login', views.login, name='login'),
    url(r'^site_options/' + SITE_SLUG + '$', views.site_options),
    url(r'^all$', views.all_sites),
)
