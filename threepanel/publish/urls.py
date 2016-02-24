from django.conf.urls import patterns, url
from . import views

EMAIL = "(?P<email>[-+_\w\.@]+)"
VERIFICATION_CODE = "(?P<verification_code>[-_\w]+)"
SITE_SLUG = "(?P<site_slug>[-_\w]+)"

urlpatterns = [
    url(r'^subscribe_email$', views.subscribe_email, name='subscribe_email'),
    url(r'^unsubscribe/'+EMAIL+'$', views.unsubscribe_email, name='unsubscribe_email'),
    url(r'^verify/'+EMAIL+'/'+VERIFICATION_CODE+'$', views.verify, name='verify'),
    url(r'^spam$', views.spam, name='spam'),
    url(r'^bad$', views.bad, name='bad'),
    url(r'^subscribe$', views.subscribe, name='subscribe'),
    url(r'^manage/' + SITE_SLUG + '$', views.manage, name='manage'),
]
