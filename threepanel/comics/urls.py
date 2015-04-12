from django.conf.urls import patterns, include, url
from django.contrib import admin

SLUG = "(?P<slug>[-_\w]+)"

urlpatterns = patterns('',
    url(r'^$', 'comics.views.home', name='home'),
    url(r'^manage', 'comics.views.manage', name='manage'),
    url(r'^create', 'comics.views.create', name='create'),
    url(r'^update/'+SLUG+'/$', 'comics.views.update', name='update'),
    url(r'^delete/'+SLUG+'/$', 'comics.views.delete', name='delete'),
)
