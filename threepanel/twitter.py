import tweepy

from dashboard.models import SiteOptions

class TwitterMessageTooLong(Exception):
    pass

def _api():
    site_options = SiteOptions.get()
    consumer_key = site_options.twitter_consumer_key.strip(" ")
    consumer_secret = site_options.twitter_consumer_secret.strip(" ")
    access_key = site_options.twitter_access_key.strip(" ")
    access_secret = site_options.twitter_access_secret.strip(" ")
    auth = tweepy.OAuthHandler(consumer_key,
                               consumer_secret)
    auth.set_access_token(access_key, access_secret)

    api = tweepy.API(auth)
    return api

def tweet(message):
    if len(message) > 140:
        raise TwitterMessageTooLong("That message is more than 140 characters")
    api = _api()
    result = api.update_status(status=message)
    print(result)

def twitterstorm():
    api = _api()

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet)
