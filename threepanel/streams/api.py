# Django Imports
from django.contrib.auth.models import User

# Third Party Imports
from tastypie.resources import ModelResource
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization, ReadOnlyAuthorization
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
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        fields = ['username']
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = ReadOnlyAuthorization()

class AccountResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = Account.objects.all()
        resource_name = 'account'
        authentication = SessionAuthentication()
        authorization = Authorization()
