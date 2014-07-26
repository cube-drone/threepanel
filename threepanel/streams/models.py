#Python Imports
import datetime

#Django Imports
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import validate_slug

#Third Party Imports
import jsonfield
import autoslug
from model_utils.managers import PassThroughManager
from model_utils.models import StatusModel
from model_utils import Choices
from positions import PositionField

class AccountQuerySet(models.query.QuerySet):
    def owned_by(self, user):
        return self.filter(owner=user)

class Account(models.Model):
    """
    The core Stream object for a user, and the base of the user's
        heirarchy. 
    Represents an entire brand, like "Cube Drone" or "Dave the Artist"
    """
    slug = models.CharField(max_length=50, 
                            unique=True,
                            validators=[validate_slug])
    title = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    visible = models.BooleanField(default=True)
    preferences = jsonfield.JSONField()
   
    objects = PassThroughManager.for_queryset_class(AccountQuerySet)()

    def __repr__(self):
        return self.slug
    def __str__(self):
        return self.__repr__()

class Stream(models.Model):
    """
    A single stream of content - like "comics" or "videos". 
    """
    account = models.ForeignKey(Account)
    slug = models.CharField(max_length=50,
                            db_index=True,
                            editable=False,
                            validators=[validate_slug])
    title = models.CharField(max_length=100, null=False)
    description = models.TextField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    visible = models.BooleanField(default=True)
    preferences = jsonfield.JSONField()

    class Meta:
        unique_together = ('account', 'slug',)

    def save(self, *args, **kwargs):
        self.user = self.account.user
        super().save(*args, **kwargs)
    
    def __repr__(self):
        return self.slug
    def __str__(self):
        return self.__repr__()

class Article(StatusModel):
    """
    A single page on the site - "Today's Comic" - 
    which will be composed of multiple Content blocks. 
    """
    stream = models.ForeignKey(Stream)
    STATUS = Choices('draft', 'published')
    datetime = models.DateTimeField(null=False, blank=False)
    slug = autoslug.AutoSlugField(populate_from=lambda instance: \
                                    str(instance.datetime.date())+"-"+\
                                    instance.title, 
                                  db_index=True, 
                                  editable=False) 
    title = models.CharField(max_length=100, null=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    visible = models.BooleanField(default=True)
    preferences = jsonfield.JSONField()
    
    def save(self, *args, **kwargs):
        self.user = self.stream.user
        super().save(*args, **kwargs)

    def __repr__(self):
        return self.slug
    def __str__(self):
        return self.__repr__()


class Content(models.Model):
    """
    A single unit of content - an image link, unit of writing, or something.
    
    The content-type will be used to determine a renderer - like
        "markdown", "image", or "youtube"
    """
    article = models.ForeignKey(Article)
    order = PositionField(collection='article')
    content_type = models.CharField(max_length=10, null=False)
    content = jsonfield.JSONField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    visible = models.BooleanField(default=True)
    preferences = jsonfield.JSONField()
    
    def save(self, *args, **kwargs):
        self.user = self.article.user
        super().save(*args, **kwargs)
    
    def __repr__(self):
        return "content-"+str(self.order)
    def __str__(self):
        return self.__repr__()
