from django.conf.urls import patterns, include, url
from tastypie.api import Api
from .api import AccountResource, StreamResource, ArticleResource, \
                 ContentResource, UserResource

api = Api(api_name='0.0.1')
api.register(AccountResource())
api.register(StreamResource())
api.register(ArticleResource())
api.register(ContentResource())
api.register(UserResource())

urlpatterns = patterns('',
    (r'api/', include(api.urls)),
    (r'^$', 'streams.views.home'),
    (r'^accounts_bloom.js$', 'streams.views.accounts_bloom'),
)
