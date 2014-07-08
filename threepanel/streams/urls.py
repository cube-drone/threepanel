from django.conf.urls import patterns, include, url
from tastypie.api import Api
from .api import AccountResource, UserResource

api = Api(api_name='0.0.1')
api.register(AccountResource())
api.register(UserResource())

urlpatterns = patterns('',
    (r'api/', include(api.urls)),
    (r'^$', 'streams.views.home'),
)
