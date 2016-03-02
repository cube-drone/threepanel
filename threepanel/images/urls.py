from django.conf.urls import url
from . import views

SITE_SLUG = "(?P<site_slug>[-_\w]+)"
IMAGE_SLUG = "(?P<image_slug>[-_\w]+)"

urlpatterns = [
    # Manage
    url(r'^manage/$', views.manage, name='manage'),
    url(r'^manage/create/$', views.create, name='create'),
    url(r'^manage/' + IMAGE_SLUG + '/trash$', views.trash, name='trash'),
    # View
    url(r'^' + IMAGE_SLUG + '$', views.view),
    url(r'^' + IMAGE_SLUG + '.thumbnail', views.thumbnail),
    url(r'^' + IMAGE_SLUG + '.original', views.original),
]
