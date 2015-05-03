from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from .models import Comic

class LatestEntriesFeed(Feed):
    title = "Latest Cube Drone "
    link = "/rss.xml"
    description = "The latest Cube Drone comics."

    def items(self):
        return Comic.archives()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.alt_text

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('comics.views.single', kwargs={'comic_slug':item.slug})
