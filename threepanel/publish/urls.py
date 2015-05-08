from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'publish.views.subscribe', name='subscribe'),
    url(r'^subscribe$', 'publish.views.subscribe_email', name='subscribe_email'),
    url(r'^unsubscribe$', 'publish.views.unsubscribe_email', name='unsubscribe_email'),
)
