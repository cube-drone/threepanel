from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^login', 'dashboard.views.login', name='login'),
    url(r'^site_options', 'dashboard.views.site_options'),
)
