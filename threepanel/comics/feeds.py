from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import escape

from .models import Comic
from .views import single
from dashboard.models import SiteOptions
from dashboard.views import domain_multiplex

class LatestEntriesFeed(Feed):
    title = ""
    link = "/rss.xml"
    description = ""

    def get_object(self, request):

        @domain_multiplex
        def request_to_site(request):
            return request.site

        site = request_to_site(request)
        try:
            self.title = site.title
            self.description = site.elevator_pitch
        except AttributeError:
            self.title = settings.SITE_TITLE
            self.description = settings.SITE_META
            return None
        return site

    def title(self, obj):
        if obj:
            return obj.title
        else:
            return settings.SITE_TITLE

    def link(self, obj):
        if obj:
            return obj.site_url
        else:
            return settings.SITE_URL

    def items(self, obj):
        if obj:
            return Comic.archives(obj)[:7]
        else:
            return []

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        site_options = item.site
        description = """
        {}<br/>

        <a href='{}'><img style='width:650px;' width='650px' src='{}' alt='{}' title='{}'/></a>

        """.format(item.promo_text,
                   item.absolute_url(),
                   item.image_url,
                   escape(item.alt_text),
                   escape(item.secret_text))

        if site_options.patreon_page:
            description += "<br/><br/><a href='{}'>Check out my Patreon page!</a>".format(site_options.patreon_page)

        try:
            twitter_username = site_options.twitterintegration.username
            description += "<br/><br/><a href='http://twitter.com/{}'>Follow me on twitter!</a>".format(twitter_username)
        except ObjectDoesNotExist:
            pass

        return description

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse(single, kwargs={'comic_slug':item.slug})
