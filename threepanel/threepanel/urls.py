from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'threepanel.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'comics.views.home', name='home'),
    url(r'^login', 'dashboard.views.login', name='login'),
    url(r'^comics/', include('comics.urls')),

)
