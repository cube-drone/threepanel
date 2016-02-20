from django.conf.urls import patterns, url

SITE_SLUG = "(?P<site_slug>[-_\w]+)"

urlpatterns = patterns('',
    url(r'^login', 'dashboard.views.login', name='login'),
    url(r'^site_options/' + SITE_SLUG + '$', 'dashboard.views.site_options'),
)
