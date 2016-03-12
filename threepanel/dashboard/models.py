import logging

from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User
from django.conf import settings

from autoslug import AutoSlugField
from slugify import slugify as slugify_wont_serialize
import tweepy
from tweepy.error import TweepError

log = logging.getLogger('threepanel.{}'.format(__name__))

def title(c):
    """
    This in response to a serialization problem with lambdas
    """
    return c.title


def slugify(s):
    return slugify_wont_serialize(s)


class SiteOptions(models.Model):
    owner = models.ManyToManyField(User)
    # Basic
    title = models.CharField(max_length=100,
                             help_text="The title of your comic")
    slug = AutoSlugField(populate_from='title',
                         unique=True,
                         db_index=True,
                         slugify=slugify)

    domain = models.CharField(max_length=100,
                              db_index=True)

    #i.e."Code & Comics, updates Tuesday & Thursday"
    tagline = models.CharField(max_length=200,
                               blank=True,
                               help_text="A short tagline for your comic")

    #i.e."Comics about software development in a small Vancouver startup.",
    elevator_pitch = models.TextField(blank=True,
                                      help_text="A Tweet-length description of your comic.")

    # Author
    #i.e. "Curtis Lassam"
    author_name = models.CharField(max_length=100,
                                   blank=True,
                                   help_text="What's the author (or author's) names?")
    #i.e. "http://curtis.lassam.net"
    author_website = models.CharField(max_length=100,
                                      blank=True,
                                      help_text="Does the author have a personal website?")

    # Google tracking code number
    # i.e. "UA-41279849-1"
    google_tracking_code = models.CharField(max_length=50, blank=True)

    # i.e. "http://www.youtube.com/user/IkoIkoComic/playlists"
    youtube_channel = models.CharField(max_length=150,
                                       blank=True,
                                       help_text="Link to your YouTube channel")

    # Patreon Page
    # i.e. "https://www.patreon.com/cubedrone"
    patreon_page = models.CharField(max_length=150,
                                    blank=True,
                                    help_text="Link to your Patreon page")


    @property
    def site_url(self):
        if self.domain and self.domain != '':
            return "http://{}".format(self.domain)
        else:
            return "http://{}.threepanel.com".format(self.slug)


    def save(self):
        if not self.domain:
            self.domain = "{}.{}".format(self.slug, settings.SITE_DOMAIN)
        super().save()
        cache.clear()

    @classmethod
    def get(cls, domain):
        """
        Given a domain, check the subdomain and http host information
        and return the associated SiteOptions object (or None, if none exists)
        """
        if domain.startswith('www.'):
            domain = domain[4:]

        if ".{}".format(settings.SITE_DOMAIN) in domain:
            subdomain = domain[:domain.find(".")]
            site_options = SiteOptions.objects.filter(slug=subdomain)
        elif settings.SITE_DOMAIN in domain:
            return None
        else:
            site_options = SiteOptions.objects.filter(domain=domain)

        if len(site_options) > 0:
            return site_options[0]
        else:
            return None

    @classmethod
    def getForUser(cls, owner):
        """
        Given a Django User object, get all sites [] that are owned by this owner.
        """
        return owner.siteoptions_set.all()


class TwitterIntegration(models.Model):
    """
    Twitter Integration with the site.
    """

    site = models.OneToOneField(SiteOptions,
                                on_delete=models.CASCADE,
                                primary_key=True)

    # Twitter
    username = models.CharField(max_length=50, default="classam")
    widget_id = models.CharField(max_length=50, default="304715092187025408")

    consumer_key = models.CharField(max_length=100, default="",
                                    help_text="Get from apps.twitter.com")
    consumer_secret = models.CharField(max_length=100, default="",
                                       help_text="Get from apps.twitter.com")
    access_key = models.CharField(max_length=100, default="",
                                  help_text="Get from apps.twitter.com")
    access_secret = models.CharField(max_length=100, default="",
                                     help_text="Get from apps.twitter.com")


    def api(self):
        consumer_key = self.consumer_key.strip(" ")
        consumer_secret = self.consumer_secret.strip(" ")
        access_key = self.access_key.strip(" ")
        access_secret = self.access_secret.strip(" ")
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)

        api = tweepy.API(auth)
        return api

    def tweet(self, message):
        if len(message) > 140:
            log.warning("Twitter message too long, truncating: {}".format(message))
        message = message[:140]
        api = self.api()
        result = api.update_status(message)
        log.info("Tweeting {}".format(result))
        return result

    def get_public_tweets(self):
        api = self.api()
        tweets = api.home_timeline()
        return tweets

    def get_status(self):
        try:
            self.get_public_tweets()
            return True, "Twitter Integration is working great!"
        except TweepError as e:
            return False, e.reason
