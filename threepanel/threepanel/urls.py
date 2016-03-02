from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings

from comics.feeds import LatestEntriesFeed
from comics import urls as comics_urls
from comics.views import manage_redirect, home
from publish.views import subscribe
from pages import urls as pages_urls
from publish import urls as publish_urls
from images import urls as images_urls
from dashboard import urls as dashboard_urls

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^manage', manage_redirect, name='manage'),
    url(r'^dashboard/', include(dashboard_urls)),
    url(r'^comics/', include(comics_urls)),
    url(r'^subscribe/', include(publish_urls)),
    url(r'^subscribe$', subscribe),
    url(r'^pages/', include(pages_urls)),
    url(r'^i/', include(images_urls)),
    url(r'rss.xml', LatestEntriesFeed()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
