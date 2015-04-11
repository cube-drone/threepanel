from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'comics.views.home', name='home'),
    url(r'^manage', 'comics.views.manage', name='manage'),
    url(r'^create', 'comics.views.create', name='create'),
    url(r'^delete/(?P<slug>[-_\w]+)/$', 'comics.views.delete', name='delete'),
)
