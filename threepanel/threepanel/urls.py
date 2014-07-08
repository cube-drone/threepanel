from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'threepanel.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'dashboard.views.home'),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^s/', include('streams.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
