from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^login', 'dashboard.views.login', name='login'),
    url(r'^site_options', 'dashboard.views.site_options'),
)
