from __future__ import absolute_import

from django.core.mail import mail_admins

from celery import shared_task

from publish.models import EmailSubscriber, SpamSpamSpamSpam
from dashboard.models import SiteOptions
from twitter import tweet

from comics.models import Comic, Blog

@shared_task
def publish():
    publog = []

    hero = Comic.hero()
    if hero.published:
        print("Nothing to see here!")
        return

    publog.append("We're publishing a comic! Hooray!")
    publog.append(str(hero))
    hero.published = True
    # this should trigger a cache-clear and re-order operation
    hero.save()

    hero = Comic.hero()
    assert(hero.order > 0)

    # send hero e-mail to subscribers
    subscribers = EmailSubscriber.subscribers()

    mails = []
    for subscriber in subscribers:
        try:
            publog.append("Sending comic to {}".format(subscriber.email))
            subscriber.send_promo_email(hero)
        except SpamSpamSpamSpam:
            publog.append("\tCan't send: SPAM limit!")
        except Exception as e:
            publog.append(e)

    # tweet hero tweet
    twitter_message = hero.twitter_message()
    publog.append("\n")
    publog.append("Tweeting: {}".format(twitter_message))
    try:
        tweet(twitter_message)
    except Exception as e:
        publog.append(e)

    # send printed report to admin
    mail_admins(subject="Published!",
                message="\n".join(publog))

    return

