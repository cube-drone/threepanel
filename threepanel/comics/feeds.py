from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from .models import Comic
from dashboard.models import SiteOptions

class LatestEntriesFeed(Feed):
    title = "Latest Cube Drone "
    link = "/rss.xml"
    description = "The latest Cube Drone comics."

    def items(self):
        return Comic.archives()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        dashboard = SiteOptions.get()
        description = """
        {}

        <a href='{}'><img style='width:650px;' width='650px' src='{}' alt='{}' title='{}'/></a>

        """.format(item.promo_text, item.absolute_url(), item.image_url, item.alt_text, item.secret_text)

        if dashboard.patreon_page:
            description += "<br/><br/><a href='{}'>Check out my Patreon page for sweet perks and stuff!</a>".format(dashboard.patreon_page)

        if dashboard.twitter_username:
            description += "<br/><br/><a href='http://twitter.com/{}'>Follow me on twitter.</a>".format(dashboard.twitter_username)

        return description

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('comics.views.single', kwargs={'comic_slug':item.slug})
