from django.db import models
from autoslug import AutoSlugField
from slugify import slugify
import datetime

BACKLOG_SIZE = 5

class Comic(models.Model):
    title = models.CharField(max_length=100, unique_for_date='posted')
    posted = models.DateTimeField(db_index=True)
    image_url = models.CharField(max_length=300)
    secret_text = models.TextField(blank=True, default="")
    alt_text = models.TextField(blank=True, default="")

    hidden = models.BooleanField(default=False)
    
    slug = AutoSlugField(populate_from=lambda c: c.title, 
                         db_index=True, 
                         slugify=slugify)
    
    def delete(self):
        self.hidden = True
        self.save()

    @classmethod
    def hero(cls):
        now = datetime.datetime.now()
        return Comic.objects.filter(hidden=False, 
                                    posted__lte=now).order_by('-posted')[0]
        

    @classmethod
    def archives(cls):
        now = datetime.datetime.now()
        return Comic.objects.filter(hidden=False, 
                                    posted__lte=now).order_by('-posted')[1:]

    @classmethod
    def backlog(cls):
        now = datetime.datetime.now()
        return Comic.objects.filter(hidden=False, 
                                    posted__gt=now).order_by('-posted')

    @classmethod
    def trash(cls):
        return Comic.objects.filter(hidden=True)

    def __str__(self):
        return "<Comic: " + self.slug + " >"
