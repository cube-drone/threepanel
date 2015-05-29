from django.conf.urls import patterns, url

COMIC_SLUG = "(?P<comic_slug>[-_\w]+)"
SLUG = "(?P<slug>[-_\w]+)"

urlpatterns = patterns('',
    # View
    url(r'^$', 'comics.views.home', name='home'),
    url(r'c/(?P<n>[0-9]+)', 'comics.views.single_by_numerical_order'),
    url(r'c/' + COMIC_SLUG, 'comics.views.single', name='single'),
    url(r'p/' + COMIC_SLUG, 'comics.views.preview', name='preview'),

    # Archives
    url(r'^archives$', 'comics.views.archives', name='archives'),
    url(r'^archives/' + SLUG, 'comics.views.tag', name='tag'),
    url(r'^search$', 'comics.views.search', name='search'),

    # Manage Comics
    url(r'^manage$', 'comics.views.manage', name='manage'),
    url(r'^manage/trash$', 'comics.views.trash', name='trash'),
    url(r'^manage/tag/'+SLUG, 'comics.views.manage_tag', name='manage_tag'),
    url(r'^manage/create$', 'comics.views.create', name='create'),
    url(r'^manage/update/' + COMIC_SLUG + '/$', 'comics.views.update', name='update'),
    url(r'^manage/delete/' + COMIC_SLUG + '/$', 'comics.views.delete', name='delete'),

    # Blogs
    url(r'^blog$', 'comics.views.blog', name='blog'),
    url(r'^manage/update/' + COMIC_SLUG + '/create_blog$', 'comics.views.create_blog', name='create_blog'),
    url(r'^manage/update/' + COMIC_SLUG + '/update_blog/' + SLUG, 'comics.views.update_blog', name='update_blog'),
    url(r'^manage/update/' + COMIC_SLUG + '/delete_blog/' + SLUG, 'comics.views.delete_blog', name='delete_blog'),

    # Videos
    url(r'^manage/update/' + COMIC_SLUG + '/create_video$', 'comics.views.create_video', name='create_video'),
    url(r'^manage/update/' + COMIC_SLUG + '/update_video/' + SLUG, 'comics.views.update_video', name='update_video'),
    url(r'^manage/update/' + COMIC_SLUG + '/delete_video/' + SLUG, 'comics.views.delete_video', name='delete_video'),
)
