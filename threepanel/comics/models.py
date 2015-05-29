import uuid
from datetime import timedelta

from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.cache import cache

from autoslug import AutoSlugField
from slugify import slugify
from djorm_fulltext.fields import VectorField
from djorm_fulltext.models import SearchManager
import markdown

"""
You're going to see the term 'Hero' a bunch in here.
I'm using "Hero" to mean "The Most Recent Comic".
"""


class Comic(models.Model):
    """
    One comic. A single image, and a little bit of meta-data, like
    alt-text, secret-text, when it was posted, what it's called...
    """
    slug = AutoSlugField(populate_from=lambda c: c.title,
                         db_index=True,
                         slugify=slugify)

    title = models.CharField(max_length=100, unique_for_date='posted',
        help_text="The title of the comic")
    posted = models.DateTimeField(db_index=True,
        help_text="The date the comic should be published")
    image_url = models.CharField(max_length=300,
        help_text="The url to the comic's image file")
    secret_text = models.TextField(blank=True, null=False, default="",
        help_text="A small amount of text that pops up below the comic")
    alt_text = models.TextField(blank=True, null=False, default="",
        help_text="""A complete transcript of the text, for screenreaders
                    and search engines""")
    promo_text = models.CharField(max_length=80, blank=True, null=False, default='',
        help_text="""A less-than-80 character promo/teaser for the comic, posted with
                     the comic on Twitter/RSS/what-have-you""")
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    hidden = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    tags = ArrayField(base_field=models.CharField(max_length=50),
                             blank=True, null=True)

    search_index = VectorField()

    objects = SearchManager(
        fields = ('title', 'alt_text', 'secret_text', 'promo_text'),
        auto_update_search_field = True)

    created = models.DateTimeField()
    updated = models.DateTimeField()

    def hide(self):
        if not self.hidden:
            self.hidden = True
            self.save()
        else:
            self.delete()

    def slugify_tags(self):
        """
        If we want people to be able to navigate to a tag url, we're going to need to be
        able to treat all of our tags as urls-
        so ["Cube Drone", "Interlude", "Butts^^^"] ==> ["cube_drone", "interlude", "butts___"]
        """
        slugified_tags = []
        if self.tags:
            for tag in self.tags:
                slugified_tags.append(slugify(tag))
        self.tags = slugified_tags

    def save(self, reorder=True):
        if not self.id:
            self.created = timezone.now()
            self.updated = timezone.now()
        self.slugify_tags()
        super().save()
        if reorder:
            self.updated = timezone.now()
            Comic.reorder()
            # We can be pretty aggressive with caching so long as
            # we completely cream the cache every time we write anything
            cache.clear()

    @property
    def is_hero(self):
        return self.id == Comic.hero().id

    @property
    def first(self):
        if Comic.hero():
            return 1
        else:
            return None

    @property
    def last(self):
        if Comic.hero():
            return Comic.hero().order
        else:
            return None

    @property
    def previous(self):
        next_order = max(self.order - 1, 0)
        if next_order > 0:
            return next_order
        else:
            return None

    @property
    def next(self):
        if Comic.hero():
            return min(self.order + 1, Comic.hero().order)
        else:
            return None

    @classmethod
    def reorder(cls):
        """
        Set the 'order' field on every Comic object in the database.
        """
        comics = Comic.objects.all().order_by('posted')
        counter = 1
        for comic in comics:
            if not comic.hidden:
                comic.order = counter
                counter += 1
            else:
                comic.order = 0
            comic.save(reorder=False)

    @classmethod
    def hero(cls):
        """
        Return the current 'hero' comic.
        """
        now = timezone.now()
        return Comic.objects.filter(hidden=False, posted__lte=now).order_by('-posted')[0]

    @classmethod
    def archives(cls):
        now = timezone.now()
        return (Comic.objects.filter(hidden=False, posted__lte=now)
                                      .order_by('-posted')
                                      .prefetch_related("blogs"))

    @classmethod
    def all_tags(cls):
        tgs = set()
        for comic in Comic.objects.filter(hidden=False):
            for tag in comic.tags:
                tgs.add(tag)
        return tgs

    @classmethod
    def backlog(cls):
        now = timezone.now()
        return (Comic.objects.filter(hidden=False, posted__gt=now)
                                       .order_by('-posted')
                                       .prefetch_related("blogs"))

    @classmethod
    def trash(cls):
        return Comic.objects.filter(hidden=True)

    @property
    def blog_posts(self):
        return self.blogs.filter(hidden=False).order_by("-created")

    @property
    def has_blogs(self):
        return len(self.blog_posts) > 0

    def __str__(self):
        return "<Comic: {}>".format(self.slug)


class Blog(models.Model):
    """
    A unit of blog content attached to a comic.
    """
    comic = models.ForeignKey('Comic', related_name="blogs")
    title = models.CharField(max_length=100,
        help_text="The title of the blog post")
    markdown = models.TextField(blank=False, null=False,
        help_text="The blog content")
    markdown_rendered = models.TextField(blank=True, null=False, default="",
        help_text="The blog content, rendered into HTML")

    hidden = models.BooleanField(default=False)

    created = models.DateTimeField()
    updated = models.DateTimeField()

    search_index = VectorField()

    objects = SearchManager(
        fields = ('title', 'markdown'),
        auto_update_search_field = True)

    slug = AutoSlugField(populate_from=lambda c: c.title,
                         db_index=True,
                         slugify=slugify)

    def __str__(self):
        return "<Blog: {}>".format(self.slug)

    def hide(self):
        self.hidden = True
        self.save()

    def render(self):
        self.markdown_rendered = markdown.markdown(self.markdown)

    def save(self):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        self.render()
        super().save()
        cache.clear()

