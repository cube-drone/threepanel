#Stdlib Imports

#Django Imports
from django.db import models
from django.contrib.auth.models import User

#Third Party Imports
import jsonfield
import autoslug
from model_utils.managers import PassThroughManager

#Local Imports

# User
#  username
#  password
#  email
#  first_name
#  last_name

class AccountQuerySet(models.query.QuerySet):
    def owned_by(self, user):
        return self.filter(owners__username=user)

class Account(models.Model):
    owners = models.ManyToManyField(User)
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

