from django.conf.urls import patterns, url

COMIC_SLUG = "(?P<comic_slug>[-_\w]+)"
SLUG = "(?P<slug>[-_\w]+)"

urlpatterns = patterns('',
    url(r'^$', 'comics.views.home', name='home'),
    url(r'c/(?P<n>[0-9]+)', 'comics.views.single_by_numerical_order'),
    url(r'c/' + COMIC_SLUG, 'comics.views.single', name='single'),
    url(r'p/' + COMIC_SLUG, 'comics.views.preview', name='preview'),
    url(r'^manage$', 'comics.views.manage', name='manage'),
    url(r'^manage/trash$', 'comics.views.trash', name='trash'),
    url(r'^manage/'+SLUG, 'comics.views.manage_tag', name='manage_tag'),
    url(r'^archives$', 'comics.views.archives', name='archives'),
    url(r'^archives/' + SLUG, 'comics.views.tag', name='tag'),
    url(r'^create$', 'comics.views.create', name='create'),
    url(r'^update/' + COMIC_SLUG + '/$', 'comics.views.update', name='update'),
    url(r'^delete/' + COMIC_SLUG + '/$', 'comics.views.delete', name='delete'),
    url(r'^update/' + COMIC_SLUG + '/create_blog$', 'comics.views.create_blog', name='create_blog'),
    url(r'^update/' + COMIC_SLUG + '/update_blog/' + SLUG, 'comics.views.update_blog', name='update_blog'),
    url(r'^update/' + COMIC_SLUG + '/delete_blog/' + SLUG, 'comics.views.delete_blog', name='delete_blog'),
)
