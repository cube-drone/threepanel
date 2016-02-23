from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User
from django.conf import settings

from autoslug import AutoSlugField
from slugify import slugify as slugify_wont_serialize


def title(c):
    """
    This in response to a serialization problem with lambdas
    """
    return c.title


def slugify(s):
    return slugify_wont_serialize(s)


class SiteOptions(models.Model):
    owner = models.ManyToManyField(User)
    domain = models.CharField(max_length=100,
                              default="cube-drone.com",
                              db_index=True)
    # Basic
    title = models.CharField(max_length=100,
                             default="Cube Drone",
                             help_text="The title of your comic")
    slug = AutoSlugField(populate_from=title,
                         default="cube-drone",
                         unique=True,
                         db_index=True,
                         slugify=slugify)

    tagline = models.CharField(max_length=200,
                               default="Code/comics, updates Tuesday & Thursday",
                               help_text="A short tagline for your comic")
    elevator_pitch = models.TextField(default="Comics about software development in a small Vancouver startup.",
                                      help_text="A Tweet-length description of your comic.")

    # Author
    author_name = models.CharField(max_length=100,
                                   default="Curtis Lassam",
                                   help_text="What's the author (or author's) names?")
    author_website = models.CharField(max_length=100,
                                      default="http://curtis.lassam.net",
                                      help_text="Does the author have a personal website?")

    # Google tracking code number
    google_tracking_code = models.CharField(max_length=50,
                                            default="UA-41279849-1")
    youtube_channel = models.CharField(max_length=150,
                                       default="http://www.youtube.com/user/IkoIkoComic/playlists")

    # Patreon Page
    patreon_page = models.CharField(max_length=150,
                                    default="https://www.patreon.com/cubedrone")

    # Twitter
    twitter_username = models.CharField(max_length=50, default="classam")
    twitter_widget_id = models.CharField(max_length=50, default="304715092187025408")

    twitter_consumer_key = models.CharField(max_length=100, default="", help_text="Get from apps.twitter.com")
    twitter_consumer_secret = models.CharField(max_length=100, default="", help_text="Get from apps.twitter.com")
    twitter_access_key = models.CharField(max_length=100, default="", help_text="Get from apps.twitter.com")
    twitter_access_secret = models.CharField(max_length=100, default="", help_text="Get from apps.twitter.com")

    def save(self):
        super().save()
        cache.clear()

    @classmethod
    def get(cls, request):
        try:
            domain = request.GET['FAKE_DOMAIN']
        except KeyError:
            domain = request.META['HTTP_HOST']

        request.domain = domain

        if ".threepanel.com" in request.domain:
            subdomain = request.domain[:request.domain.find(".")]
            site_options = SiteOptions.objects.filter(slug=subdomain)
        elif settings.DEBUG:
            request.domain = settings.DEBUG_DOMAIN
            site_options = SiteOptions.objects.filter(domain=request.domain)
        else:
            site_options = SiteOptions.objects.filter(domain=request.domain)

        if len(site_options) > 0:
            return site_options[0]
        else:
            return None

    @property
    def site_url(self):
        if self.domain and self.domain != '':
            return "http://{}".format(self.domain)
        else:
            return "http://{}.threepanel.com".format(self.slug)
