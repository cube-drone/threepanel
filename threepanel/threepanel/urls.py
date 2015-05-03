from django.conf.urls import patterns, include, url
from comics.feeds import LatestEntriesFeed

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'threepanel.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'comics.views.home', name='home'),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^comics/', include('comics.urls')),
    url(r'rss.xml', LatestEntriesFeed())
)
