from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^login$', 'dashboard.views.login_view'),
    url(r'^logout$', 'dashboard.views.logout_view'),
    url(r'^register$', 'dashboard.views.register'),
    url(r'^users_bloom.js$', 'dashboard.views.users_bloom'),
)
