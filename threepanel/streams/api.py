# Django Imports
from django.contrib.auth.models import User

# Third Party Imports
from tastypie.resources import ModelResource
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization, ReadOnlyAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields

# Local Imports 
from .models import Account, Stream, Article, Content

class UserObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)
    def read_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user
    def create_list(self, object_list, bundle):
        return object_list
    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user
    def update_list(self, object_list, bundle):
        allowed = []

        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed
    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user
    def delete_list(self, object_list, bundle):
        return object_list
    def delete_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

class UserResource(ModelResource):
    accounts = fields.ToManyField('streams.api.AccountResource', 'account_set')
    streams = fields.ToManyField('streams.api.StreamResource', 'stream_set')
    articles = fields.ToManyField('streams.api.ArticleResource', 'article_set')
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username']
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = ReadOnlyAuthorization()
        always_return_data = True

class AccountResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    streams = fields.ToManyField('streams.api.StreamResource', 'stream_set')
    class Meta:
        queryset = Account.objects.all()
        resource_name = 'account'
        authentication = SessionAuthentication()
        authorization = UserObjectsOnlyAuthorization()
        always_return_data = True

class StreamResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    account = fields.ForeignKey(AccountResource, 'account')
    articles = fields.ToManyField('streams.api.ArticleResource', 'article_set')
    class Meta:
        queryset = Stream.objects.all()
        resource_name = 'stream'
        authentication = SessionAuthentication()
        authorization = UserObjectsOnlyAuthorization()
        always_return_data = True
        filtering = {
            'account':ALL_WITH_RELATIONS,
            'slug':ALL,
        }

class ArticleResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    stream = fields.ForeignKey(StreamResource, 'stream')
    content = fields.ToManyField('streams.api.ContentResource', 'content_set')
    class Meta:
        queryset = Article.objects.all()
        resource_name = 'article'
        authentication = SessionAuthentication()
        authorization = UserObjectsOnlyAuthorization()
        always_return_data = True
        filtering = {
            'stream':ALL_WITH_RELATIONS,
            'slug':ALL,
        }

class ContentResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    article = fields.ForeignKey(ArticleResource, 'article')
    class Meta:
        queryset = Content.objects.all()
        resource_name = 'content'
        authentication = SessionAuthentication()
        authorization = UserObjectsOnlyAuthorization()
        always_return_data = True
        filtering = {
            'article':ALL_WITH_RELATIONS,
            'slug':ALL,
        }
