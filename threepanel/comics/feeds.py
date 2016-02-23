from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from .models import Comic
from dashboard.models import SiteOptions
from django.conf import settings

class LatestEntriesFeed(Feed):
    title = "Latest Cube Drone "
    link = "/rss.xml"
    description = "The latest Cube Drone comics."

    def get_object(self, request):
        return SiteOptions.get(request)

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
        return Comic.archives(obj)[:7]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        dashboard = item.site
        description = """
        {}

        <a href='{}'><img style='width:650px;' width='650px' src='{}' alt='{}' title='{}'/></a>

        """.format(item.promo_text, item.absolute_url(), item.image_url, item.alt_text, item.secret_text)

        if dashboard.patreon_page:
            description += "<br/><br/><a href='{}'>Check out my Patreon page!</a>".format(dashboard.patreon_page)

        if dashboard.twitter_username:
            description += "<br/><br/><a href='http://twitter.com/{}'>Follow me on twitter!</a>".format(dashboard.twitter_username)

        return description

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('comics.views.single', kwargs={'comic_slug':item.slug})
