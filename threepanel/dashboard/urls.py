from django.conf.urls import patterns, url
from . import views

SITE_SLUG = "(?P<site_slug>[-_\w]+)"

urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^manage/' + SITE_SLUG + '/site_options$', views.site_options),
    url(r'^manage/' + SITE_SLUG + '/site_options/twitter$', views.twitter_integration),
    url(r'^all$', views.all_sites),
]
