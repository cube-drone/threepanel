from django.conf.urls import patterns, url

SLUG = "(?P<slug>[-_\w]+)"

urlpatterns = patterns('',
    url(r'^$', 'comics.views.home', name='home'),
    url(r'c/(?P<n>[0-9]+)', 'comics.views.single_by_numerical_order'),
    url(r'c/' + SLUG, 'comics.views.single', name='single'),
    url(r'^manage', 'comics.views.manage', name='manage'),
    url(r'^create', 'comics.views.create', name='create'),
    url(r'^update/' + SLUG + '/$', 'comics.views.update', name='update'),
    url(r'^delete/' + SLUG + '/$', 'comics.views.delete', name='delete'),
)
