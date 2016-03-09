from unittest.mock import patch, MagicMock

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.conf import settings

from .models import SiteOptions, TwitterIntegration
from .views import twitter_integration

# Create your tests here.

class TwitterTestCase(TestCase):
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

        self.twitter = TwitterIntegration(site=self.site,
                                          username="testy",
                                          widget_id="TWITTER_WIDGET_ID",
                                          consumer_key="TWITTER_CONSUMER_KEY",
                                          consumer_secret="TWITTER_CONSUMER_SECRET",
                                          access_key="TWITTER_ACCESS_KEY",
                                          access_secret="TWITTER_ACCESS_SECRET")

        self.factory = RequestFactory()

    def test_object_creation(self):
        self.assertEqual(self.twitter.username, "testy")

    @patch('tweepy.OAuthHandler')
    @patch('tweepy.API')
    def test_tweep(self, api_mock, oauth_mock):
        api = self.twitter.api()
        oauth_mock.assert_called_with("TWITTER_CONSUMER_KEY", "TWITTER_CONSUMER_SECRET")
        api_mock.assert_called()

    def test_message(self):
        api_mock = MagicMock()
        self.twitter.api = MagicMock()
        self.twitter.api.return_value = api_mock

        self.twitter.tweet("Hello")
        api_mock.update_status.assert_called_with("Hello")

    def test_truncate_message(self):
        api_mock = MagicMock()
        self.twitter.api = MagicMock()
        self.twitter.api.return_value = api_mock

        self.twitter.tweet("A"*200)
        api_mock.update_status.assert_called_with("A"*140)

    def test_is_working(self):
        is_working, message = self.twitter.get_status()
        self.assertFalse(is_working)
        self.assertTrue("Invalid or expired token" in message)

    def test_twitter_integration_view(self):
        request = self.factory.get('/dashboard/manage/test_comic/site_options/twitter')

        request.user = self.user

        response = twitter_integration(request, self.site.slug)
        self.assertEqual(response.status_code, 200)
