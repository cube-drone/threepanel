from django.conf.urls import patterns, url

SLUG = "(?P<slug>[-_\w]+)"

urlpatterns = patterns('',
    # View
    url(r'^'+SLUG+'$', 'pages.views.page', name='page')
)
