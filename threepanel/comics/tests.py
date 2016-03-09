from unittest.mock import patch, MagicMock

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from django.conf import settings
from django.utils import timezone

from dashboard.models import SiteOptions
from .models import Comic
from .tasks import publish
from .feeds import LatestEntriesFeed

# Create your tests here.

class ComicsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testy',
                                             email='testytesterson@sample.org',
                                             password='top_secret')
        self.site = SiteOptions(title="Test Comic",
                                domain="testcomic.org",
                                tagline="The testyest comic of them all.",
                                elevator_pitch="It's a blerg for your blarg!",
                                author_name="Testy Testerson",
                                author_website="http://testy.sample.org",
                                google_tracking_code="",
                                youtube_channel="",
                                patreon_page="")
        self.site.save()

        self.comic = Comic(site=self.site,
                           title="Publish Test",
                           image_url="http://test.image",
                           secret_text="butts",
                           alt_text="butts",
                           promo_text="butts",
                           posted=timezone.now())
        self.comic.save()

        self.factory = RequestFactory()

    def test_object_creation(self):
        self.assertEqual(self.comic.title, "Publish Test")

    def test_publish(self):
        publish()

    def test_rss(self):
        request = self.factory.get('/rss.xml')

        request.user = AnonymousUser()

        # Use this syntax for class-based views.
        request.META['HTTP_HOST'] = 'testcomic.org'
        response = LatestEntriesFeed()(request)
        self.assertEqual(response.status_code, 200)
