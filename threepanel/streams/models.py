#Stdlib Imports

#Django Imports
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

#Third Party Imports
import jsonfield
import autoslug
from model_utils.managers import PassThroughManager

class AccountQuerySet(models.query.QuerySet):
    def owned_by(self, user):
        return self.filter(owners__username=user)

class Account(models.Model):
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100, null=False)
    slug = autoslug.AutoSlugField(populate_from='title')
    preferences = jsonfield.JSONField()
    
    @classmethod
    def create_account(cls, user, title):
        account = cls(title=title)
        account.save()
        account.owners.add(user)
        account.save()
        return account
    
    objects = PassThroughManager.for_queryset_class(AccountQuerySet)()

